; crypto suite selection demo.
;     To execute: load, reset and run.

; vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab:lisp

; cryptography objects

(deftemplate cipher
    (slot algorithm
        (type SYMBOL)
        (allowed-symbols AES IDEA 3DES DES RC4 Serpent Blowfish Camellia)
        (default ?NONE))
    (slot keysize
        (type INTEGER))
    )

(deftemplate hash
    (slot algorithm
        (type SYMBOL)
        (allowed-symbols MD5 SHA1 SHA256 SHA512)
        (default ?NONE))
    (slot keysize
        (type INTEGER))
    )

(deftemplate authentication
    (slot algorithm
        (type SYMBOL)
        (allowed-symbols RSA DSA ECDSA)
        (default ?NONE))
    )

(deftemplate keyexchange
    (slot algorithm
        (type SYMBOL)
        (allowed-symbols RSA DH ECDH SRP PSK)
        (default ?NONE))
    )

; policy objects
;Pre-Activated Key Retention Time: Time until preactivated keys are destroyed if not used
;Active Key Retention Time: Time until active keys move to deactivated state
;Deactivated Key Retention Time:Time until deactivated keys move to destroyed state
;Compromised Key Retention Time:Time until compromised keys move to destroyed-compromised state

; Client Lease Times

(deftemplate keystate
    (slot state
        (type SYMBOL)
        (allowed-symbols pre-active active deactivated destroyed compromised destroyed-compromised)
        (default pre-active))
    )

(defclass Ciphersuite
  (is-a USER)
  (slot auth (type INSTANCE))
  (slot cipher (type INSTANCE))
  (slot hash (type INSTANCE))
  )

(defclass Certificate
  (is-a OBJECT)
)

;(deftemplate key
;    (slot state
;       (type OBJECT))
;    (slot cipher
;       (type OBJECT))
;    )

(defclass Key
  (is-a USER)
  (slot uuid
     (type STRING) (default ?NONE))
  (slot state
     (type INSTANCE))
  (slot cipher
     (type INSTANCE))
  (slot expired
     (type SYMBOL) 
        (allowed-symbols true false) 
        (default false)
        (create-accessor read-write))
  )

(defmessage-handler Key expire () (bind ?self:expired true))

(defclass Policy
  (is-a USER)
  (slot key (type INSTANCE))
  (slot pre-active-expiretime
     (type FLOAT))
  )

(deftemplate group
    (multislot name
        (type STRING))
    )

;;; acceptance


;;; sample app rules

(defrule is-md5 ""
    (hash (algorithm MD5))
  =>
    (setstate1 "Is MD5"))


(defrule policy-key-expired ""
     (object (is-a Policy) (pre-active-expiretime ?exp&:(> ?exp (now))))
     ?k <- (object)
     =>
     (send ?k set-expired true))


(defrule is-aes256 ""
    (cipher (keysize 256) (algorithm AES))
  =>
    (setstate2 "Is AES-256")
)

(defrule good-pki ""
     (hash (algorithm SHA256) (keysize 2048))
    =>
    (setstate3 "Good PKI")
)

(defrule no-hash-md5 ""
    (not (hash (algorithm MD5)))
  =>
    (setstate1 "Is MD5")
    (assert (acceptable false)))

; Assert initial facts in an empty rule.
; These facts
(defrule startup ""
    =>
    (assert (acceptable false))
    (assert (group (name "group1")))
    (assert (cipher (keysize 256) (algorithm AES)))
    (assert (hash (algorithm SHA1)))
;    (assert (hash (algorithm SHA256) (keysize 2048)))
    )

;(make-instance key1 of Key (uuid "abcd") )
;(make-instance key1 of Key (uuid "abcd") (state keystate (state pre-active) ))
;(make-instance p of Policy (key (make-instance (gensym) of Key (uuid "abcd") (pre-active-expiretime (+ (now) 100)))))

