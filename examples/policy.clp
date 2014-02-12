; crypto suite selection demo.
;     To execute: load, reset and run.

; cryptography objects

(deftemplate cipher
    (multislot algorithm
        (type SYMBOL)
        (allowed-symbols AES IDEA 3DES DES RC4 Serpent Blowfish Camellia)
        (default AES))
    (multislot keysize
        (type INTEGER))
    )

(deftemplate hash
    (multislot algorithm
        (type SYMBOL)
        (allowed-symbols MD5 SHA1 SHA256 SHA512)
        (default SHA256))
    )

(deftemplate authentication
    (multislot algorithm
        (type SYMBOL)
        (allowed-symbols RSA DSA ECDSA)
        (default RSA))
    )

(deftemplate keyexchange
    (multislot algorithm
        (type SYMBOL)
        (allowed-symbols RSA DH ECDH SRP PSK)
        (default DH))
    )

; policy objects

(deftemplate group
    (multislot name
        (type STRING))
    )

; acceptance



;;; sample app rules

(defrule is-md5 ""
    (hash (algorithm MD5))
  =>
    (setstate1 "Is MD5"))

(defrule is-aes256 ""
    (cipher (keysize 256) (algorithm AES))
  =>
    (setstate2 "Is AES-256"))

;(defrule no-hash-md5 ""
;    (not hash (algorithm MD5))
;  =>
;    (setstate1 "Is MD5")
;    (assert (acceptable false)))

; Assert initial facts in an empty rule.
; These facts
(defrule startup ""
    =>
    (assert (acceptable false))
    (assert (group (name "group1")))
    (assert (cipher (keysize 256) (algorithm AES)))
    (assert (hash (algorithm SHA1)))
    )

