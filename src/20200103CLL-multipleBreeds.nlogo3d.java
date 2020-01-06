;;;;;;;;;;;;;;;;;;
;;;;; BREEDS ;;;;;
;;;;;;;;;;;;;;;;;;

breed [ NeedSignalCancerCells NeedSignalCancerCell ]
breed [ BlockedApoCancerCells BlockedApoCancerCell ]
breed [ EarlyApoCancerCells EarlyApoCancerCell ]
breed [ LateApoCancerCells LateApoCancerCell ]
breed [ DeadCancerCells DeadApoCancerCell ]
breed [ Monocytes Monocyte ]
breed [ NurseLikeCells NurseLikeCell ]



;;;;;;;;;;;;;;;;;;;;;
;;;;; VARIABLES ;;;;;
;;;;;;;;;;;;;;;;;;;;;

globals [
  ;; create limits of the world
  z-max
  coef

  ;; global variables for headless mode
  simulation-duration
  prop-world-filled-init
  nb-monocytes-init
  nb-cancer-cells-init
  prop-monocytes-init
  prop-apoptotic-init
  BlockedApoptosisThreshold
  Chemical_B_threshold
  EarlyApoThreshold
  LateApoThreshold
  DeathThreshold
]

patches-own [
  forbidden ;; manual fix to prevent auto-wrapping
  Chemical_A ;; chemical excreted by Monocytes and NurseLikeCells transmitting anti-apoptotic signals to B cells.
  Chemical_B ;; chemical excreted by NeedSignalCancerCells transmitting differentiation signals to Monocytes.
  ;; Monocytes will increase their signal strength depending on Chemical_B, and will further secrete more Chemical_A.
]

NeedSignalCancerCells-own[
  Chemical_N ;; accumulated necrotic factors
  Chemical_S ;; accumulated survival signals
]

BlockedApoCancerCells-own[
  Chemical_N ;; accumulated necrotic factors (stabilized to 0)
  Chemical_S ;; accumulated survival signals
]

EarlyApoCancerCells-own[
  Chemical_N ;; accumulated necrotic factors
  Chemical_S ;; accumulated survival signals
]

LateApoCancerCells-own[
  Chemical_N ;; accumulated necrotic factors
  Chemical_S ;; accumulated survival signals
]

DeadCancerCells-own[
  Chemical_N ;; accumulated necrotic factors
  Chemical_S ;; accumulated survival signals
]

Monocytes-own[
  SignalStrength ;; potentiates the excretion of Chemical_A
]

NurseLikeCells-own[
  SignalStrength ;; potentiates the excretion of Chemical_A (stabilized to 100)
]


;;;;;;;;;;;;;;;;;
;;;;; SETUP ;;;;;
;;;;;;;;;;;;;;;;;

to setup
  clear-all
  reset-ticks
  let seed 12
  random-seed seed

  setup-Globals

  setup-World
  setup-Monocytes
  setup-NeedSignalCancerCells

end



to setup-Globals
  set prop-world-filled-init gui-prop-world-filled-init
  set nb-cancer-cells-init gui-nb-cancer-cells-init
  set prop-monocytes-init gui-prop-monocytes-init
  set prop-apoptotic-init gui-prop-apoptotic-init

  ;; NeedSignalCancerCells need to accumulate some amount of Chemical_A anti-apoptotic signal from Monocytes and/or NLCs to enter BlockedApoptosis
  set BlockedApoptosisThreshold gui-BlockedApoptosisThreshold

  ;; Monocytes need to accumulate some amount of Chemical_B from NeedSignalCancerCells cancer cells to increase their SignalStrength and eventually differentiate into NLCs
  set Chemical_B_threshold gui-NLC_threshold

  ;; NeedSignalCancerCells turn into EarlyApoCancerCells when they reach necrotic value 1
  set EarlyApoThreshold gui-EarlyApoThreshold

  ;; EarlyApoCancerCells turn into LateApoCancerCells when they reach necrotic value 2
  set LateApoThreshold gui-LateApoThreshold

  ;; LateApoCancerCells turn into DeadCancerCells when they reach necrotic value 3
  set DeathThreshold gui-DeathThreshold

end


to setup-World
  ;; get initial number of cells
  set nb-monocytes-init ceiling (prop-monocytes-init * nb-cancer-cells-init / 100)
  let nb-cells-init nb-cancer-cells-init + nb-monocytes-init

  ;; resize the simulation world
  set z-max 1
  set coef 4
  let world-radius ceiling sqrt (nb-cells-init * 100 / (prop-world-filled-init * pi * (z-max * 2 + 1)))
  resize-world (- world-radius * coef) (world-radius * coef) (- world-radius * coef) (world-radius * coef) (- z-max * coef) (z-max * coef)

  ;; close the world
  ;; only not forbidden patches are accessible to the agents
  ask patches [
    ifelse ((pxcor * pxcor + pycor * pycor) > (world-radius * world-radius) or abs pzcor > z-max)
    [ set forbidden true ]
    [ set forbidden false
      set Chemical_A 0
      set Chemical_B 0
      ;;recolor-patch
    ]
  ]

   ;; create NeedSignalCancerCells
  ask n-of nb-cells-init (patches with [not forbidden]) [ sprout-NeedSignalCancerCells 1 ]

end

to recolor-patch  ;; patch procedure
  ;; give color to chemical sources
  ;; scale color to show chemical concentration
  set pcolor scale-color green Chemical_A -20 200
  ;;set pcolor scale-color red Chemical_B -20 200
end

to setup-Monocytes
  ;; create Monocytes
  ask n-of nb-monocytes-init turtles
  [
    set breed Monocytes
    set Chemical_A 0
    set SignalStrength 0
    set color blue
    set shape "square"
  ]
end

to setup-NeedSignalCancerCells
  ask NeedSignalCancerCells [
    set Chemical_S 0 ;; random (BlockedApoptosisThreshold)
    set Chemical_N 0 ;; random (EarlyApoThreshold)
    set color red
    set shape "default"
    set size 1
  ]

  ;; create some EarlyApoCancerCells at random values before EarlyApoThreshold
  ask n-of (prop-apoptotic-init * nb-cancer-cells-init / 100) NeedSignalCancerCells
  [
  set breed EarlyApoCancerCells
    set Chemical_N random EarlyApoThreshold
    set Chemical_S 0
    set color orange
    set shape "default"
  ]
  end


;;UTILS

to phagocyte
    ;; look for dead or late apoptotic cells in the neighbors
    let debris (turtle-set (DeadCancerCells-on neighbors) (LateApoCancerCells-on neighbors))
    ifelse (any? debris)
    ;; phagocyte
    [ ask one-of debris [die] ]
    [ move 1 nobody ]
end

to move [steps goal] ;; agent procedure
  ifelse (goal != nobody)
  ;; move towards goal
  [
    while [steps > 0] [
      ;; distance from the agent to the goal
      let current-distance distance goal
      ;; find neighbors who are closer to the goal
      let closer-positions neighbors with [not forbidden and
                                           not any? turtles-here and
                                           distance goal <= current-distance and
                                           distance goal > 1]
      ifelse (any? closer-positions)
      ;; move closer to the goal
      [
        move-to min-one-of closer-positions [distance goal]
        set steps steps - 1
      ]
      ;; impossible to move closer, stay put
      [ set steps 0 ]
    ]
  ]
  ;; random move
  [
    while [steps > 0] [
      ;; find accessible positions
      let possible-positions neighbors with [not forbidden and not any? turtles-here]
      ifelse (any? possible-positions)
      ;; move
      [
        move-to one-of possible-positions
        set steps steps - 1
      ]
      ;; impossible to move closer, stay put
      [ set steps 0 ]
    ]
  ]
end

to move-to-chemical ;; cancer cell procedure
  let current-distance distance max_Chemical_A
  ;;let closer-positions neighbors with [not forbidden and
                                           ;;not any? turtles-here and
                                           ;;distance max_Chemical_A <= current-distance and
                                           ;;distance max_Chemical_A > 1]
  let possible-positions neighbors with [not forbidden and not any? turtles-here and Chemical_A > 0]
  ;;ifelse (any? closer-positions)
  ifelse (any? possible-positions)
  [ move-to max_Chemical_A ]
  [ move 6 nobody ]

end

to-report max_Chemical_A ;; cancer cell procedure
  ;; sniff around, and report where the strongest smell is
  let possible-patches neighbors with [not forbidden and not any? turtles-here]
  let max-chemical-patches possible-patches with-max [Chemical_A]
  ifelse (any? max-chemical-patches)
  [report one-of max-chemical-patches]
  [report one-of neighbors]
end

;;;;;;;;;;;;;;
;;;;; GO ;;;;;
;;;;;;;;;;;;;;



to go
  reset-timer
  ifelse (count NeedSignalCancerCells + count EarlyApoCancerCells + count LateApoCancerCells + count BlockedApoCancerCells > 0)
  [
    common-go-procedures
    tick
  ]
  [ stop ]
end

to common-go-procedures ;; between headless and gui modes

  update-positions

  update-chemicals

  update-breeds

end

to update-positions

  ;; NeedSignalCancerCells actions
  ;; BlockedApoCancerCells actions
  ;; EarlyApoCancerCells actions
  ;; LateApoCancerCells actions
  ;; Monocytes actions
  ;; NurseLikeCells actions

  ;; NeedSignalCancerCells actions
  ask NeedSignalCancerCells
  [ move-to-chemical ]

  ;; BlockedApoCancerCells actions
  ask BlockedApoCancerCells
  [ move 6 nobody ]

  ;; EarlyApoCancerCells actions
  ask EarlyApoCancerCells
  [ move-to-chemical ]

  ;; LateApoCancerCells actions
  ask LateApoCancerCells
  [ move-to-chemical ]

  ;; Monocytes actions
  ask Monocytes
  [ phagocyte ]

  ;; NurseLikeCells actions
  ask NurseLikeCells
  [ phagocyte ]

end

to update-chemicals

  diffuse chemical_A (diffusion-rate / 100)
  diffuse chemical_B (diffusion-rate / 100)

  ;; Patches actions
  ask patches
  [
    set chemical_A chemical_A * (100 - evaporation-rate) / 100  ;; slowly evaporate chemical_A
    set chemical_B chemical_B * (100 - evaporation-rate) / 100  ;; slowly evaporate chemical_B
    ;;recolor-patch
  ]

  ;; NeedSignalCancerCells actions
  ask NeedSignalCancerCells
  [
    set Chemical_B Chemical_B + 1 ;; drop some Chemical_B
    set Chemical_N Chemical_N + 1 ;; accumulate some Chemical_N
    if ( [Chemical_A] of patch-here > 0 )
    [
      set Chemical_S Chemical_S + 1 ;; accumulate some Chemical_S via the absorption of Chemical_A which increases survival (anti-apoptotic signal)
      ;; we might need to substract the Chemical_A from the patch if its absorbed by the B cell
      set Chemical_A Chemical_A - 1
    ]
  ]

  ;; BlockedApoCancerCells actions
  ask BlockedApoCancerCells
  [
    ;; as long as they walk on patches with some Chemical_A, no change;
    ;; but when they walk on an empty patch, their Chemical_S decreases.
    if ( [Chemical_A] of patch-here <= 0 ) [ set Chemical_S Chemical_S - 1 ]
  ]

  ;; EarlyApoCancerCells actions
  ask EarlyApoCancerCells
  [
    set Chemical_N Chemical_N + 1 ;; accumulate some Chemical_N
    set Chemical_S Chemical_S + 1 ;; accumulate some Chemical_S via the absorption of Chemical_A which increases survival (anti-apoptotic signal)
    ;; we might need to substract the Chemical_A from the patch if its absorbed by the B cell
  ]

  ;; LateApoCancerCells actions
  ask LateApoCancerCells
  [
    set Chemical_N Chemical_N + 1 ;; accumulate some Chemical_N
  ]

  ;; Monocytes actions
  ask Monocytes
  [;; update SignalStrength based on Chemical_B
    update-SignalStrength-BasedOnChemical_B 
    set Chemical_A Chemical_A + SignalStrength / 10 ;; drop some Chemical_A based on the cell signalling power (signal strength)
  ]

  ;; NurseLikeCells actions
  ask NurseLikeCells
  [ ;; if Potentiated State is reached by the Monocyte, it is a NLC,
    if (SignalStrength >= Chemical_B_threshold) 
    [
      set Chemical_A Chemical_A + SignalStrength ;; then drop more Chemical_A than a monocyte, here 10x times more. TODO : make proportional setting from interface !!
      
      if ( [Chemical_B] of patch-here <= 0 )
      [ set SignalStrength SignalStrength - 1 ]
    ]
    ;;else?
  ]

end

to update-SignalStrength-BasedOnChemical_B
    ;; update SignalStrength based on Chemical_B
    ifelse ( [Chemical_B] of patch-here <= 0 )
    [ set SignalStrength SignalStrength - 1 ]
    [ 
      set SignalStrength SignalStrength + 1 
      ;; we might need to substract this Chemical_B amount from the patch
      set Chemical_B Chemical_B - 1
    ] 
end


to update-breeds
  ;; NeedSignalCancerCells
  ask NeedSignalCancerCells
  [
    if ( Chemical_N >= EarlyApoThreshold )
    [
      ;; change from NeedSignalCancerCell to EarlyApoCancerCell
      set breed EarlyApoCancerCells
      set color orange
      set shape "default"
      set Chemical_N Chemical_N
      set Chemical_S Chemical_S
    ]

    if ( Chemical_S >= BlockedApoptosisThreshold)
    [
      ;; change from NeedSignalCancerCell to BlockedApoCancerCell
      set breed BlockedApoCancerCells
      set color pink
      set shape "default"
      set Chemical_N 0
      set Chemical_S Chemical_S
    ]
  ]

  ;; EarlyApoCancerCells
  ask EarlyApoCancerCells
  [
    if ( Chemical_N >= LateApoThreshold )
    [
      ;; change from EarlyApoCancerCell to LateApoCancerCell
      set breed LateApoCancerCells
      set color yellow
      set shape "default"
      set Chemical_N Chemical_N
      set Chemical_S 0
    ]
  ]

  ;; LateApoCancerCells
  ask LateApoCancerCells
  [
    if ( Chemical_N >= DeathThreshold )
    [
      ;; change from LateApoCancerCell to DeadCancerCell
      set breed DeadCancerCells
      set color grey
      set shape "default"
      set Chemical_N Chemical_N ;; (should have reached the max Chemical_N value ie DeathThreshold)
      set Chemical_S 0
    ]
  ]

  ;; BlockedApoCancerCells
  ask BlockedApoCancerCells
  [
    if ( Chemical_S < BlockedApoptosisThreshold )
    [
      ;; change from BlockedApoCancerCell to NeedSignalCancerCell
      set breed NeedSignalCancerCells
      set color red
      set shape "default"
      set Chemical_N 0
      set Chemical_S 0
    ]
  ]

  ;; Monocytes
  ask Monocytes
  [
    if ( SignalStrength >= gui-NLC_threshold )
    [
      ;; change from Monocyte to NurseLikeCells
      set breed NurseLikeCells
      set color green
      set shape "square"
      set SignalStrength SignalStrength
    ]
  ]

  ;; NurseLikeCells
  ask NurseLikeCells
  [
    if ( SignalStrength < gui-NLC_threshold )
    [
      ;; change from Monocyte to NurseLikeCells
      set breed Monocytes
      set color blue
      set shape "square"
      set SignalStrength SignalStrength
    ]
  ]

end