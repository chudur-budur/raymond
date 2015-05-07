;; This buffer is for notes you don't want to save, and for Lisp evaluation.
;; If you want to create a file, visit that file with C-x C-f,
;; then enter the text in that file's own buffer.

;; with meWeight = 0.3 and progWeight = 0.7 -- better than raymond's algorithm
;; for all test cases, why ??
(progn2 
 (if (and (and is-waiting-for-token is-regreq) (not is-regreq)) 
     (send-token-to holder)) 
 (progn2 
  (if-else (and want-cs is-regreq)
	   (progn2 
	    (if (and (and is-waiting-for-token is-regreq) (not is-regreq)) 
		(send-token-to holder)) 
	    (if-else (not (or (not is-regreq) has-token)) 
		     (send-req-to q-top) 
		     (if-else (and want-cs is-regreq) 
			      (if is-q-empty exit-cs)
			      (if has-token enter-cs))))
	   enter-cs)
  (if-else (not (or is-regreq has-token)) 
	   (if is-q-empty exit-cs) 
	   (if-else (and want-cs is-regreq)
		    (if is-q-empty exit-cs) 
		    (if has-token enter-cs)))))

(progn2 
 (if (and (and is-waiting-for-token is-regreq) (not is-regreq)) 
     (send-token-to holder)) 
 (progn2 
  (if-else (and want-cs is-regreq)
	   (progn2 
	    (if (and (and is-waiting-for-token is-regreq) (not is-regreq)) 
		(send-token-to holder)) 
	    (if-else (not (or (not is-regreq) has-token)) 
		     (send-req-to q-top) 
		     (if-else (and want-cs is-regreq) 
			      (if is-q-empty exit-cs)
			      (if has-token enter-cs))))
	   enter-cs)

;; this is also givin good results, why ??
(if-else (or (and is-waiting-for-token want-cs)
	     (not (or has-token is-incs))) 
	 (progn2 
	  (progn2
	   (progn2 exit-cs exit-cs) 
	   (progn2 
	    (progn2 exit-cs exit-cs) 
	    (if want-cs register-req-q)))
	  (progn2 
	   enter-cs 
	   exit-cs)) 
	 (progn2 enter-cs
		 exit-cs))

;; this is also, why ?
(if-else (or (and (or is-incs is-incs) 
		  (and is-waiting-for-token want-cs)) 
	     (not (or has-token is-incs))) 
	 (progn2 
	  (if (not is-holder) (progn2 exit-cs enter-cs)) 
	  (progn2 (progn2 exit-cs exit-cs) 
		  (if want-cs register-req-q)))
	 (send-token-to q-top))

