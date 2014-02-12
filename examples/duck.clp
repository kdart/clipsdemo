(defrule ideal-duck-bachelor
    (bill big ?name)
    (feet wide ?name)
  =>
    (printout t "The ideal duck is " ?name crlf))
(deffacts duck-assets
    (bill big Dopey)
    (bill big Dorky)
    (bill little Dicky)
    (feet wide Dopey)
    (feet narrow Dorky)
    (feet narrow Dicky))


