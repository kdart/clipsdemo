
(defrule is-reset1 ""
    ?s <- (state1-is-reset)
=>
    (printout t "state1 is reset" crlf)
    (setstate1 "NewState1")
    (retract ?s)
)

(defrule start ""
  =>
    (printout t (getstate1) crlf)
    (printout t (getstate2) crlf)
    (printout t (getstate3) crlf)
    (printout t (getstate4) crlf)
    (assert (state1-is-reset))
    )

