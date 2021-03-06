;; This buffer is for notes you don't want to save, and for Lisp evaluation.
;; If you want to create a file, visit that file with C-x C-f,
;; then enter the text in that file's own buffer.

;; with mutexWeight = 0.3 and progressWeight = 0.7 -- better than raymond's algorithm
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

;; this is another one with mutexWeight = 0.4, progressWeight = 0.6
(progn2 (if-else (and want-cs is-regreq)
		 (if is-q-empty exit-cs) enter-cs) 
	(if-else (not (or is-regreq has-token)) 
		 (if is-q-empty exit-cs) 
		 (if-else (and want-cs is-regreq)
			  (if is-q-empty exit-cs) 
			  (progn2 
			   (progn2 (if (and (and is-waiting-for-token is-regreq) (not is-regreq)) 
				       (send-token-to holder))
				   (progn2 (if-else (and want-cs is-regreq)
						    (send-token-to holder) enter-cs) 
					   (progn2
					    (if (not is-regreq) enter-cs) 
					    (progn2 
					     (if-else (and want-cs is-regreq) 
						      (send-token-to holder)
						      enter-cs) 
					     (if-else (and want-cs is-regreq)
						      (send-token-to holder) 
						      enter-cs))))) 
			   (if (and (and want-cs is-regreq) (not is-regreq))
			       (send-token-to holder))))))

;; this is also, with mutexWeight = 0.5, progressWeight = 0.5
(progn2 (if-else (and want-cs is-regreq)
		 (send-token-to holder) enter-cs) 
	(if-else (not (or is-regreq has-token)) 
		 (if is-q-empty exit-cs) 
		 (if-else (and want-cs is-regreq)
			  (if is-q-empty exit-cs) 
			  (progn2 
			   (progn2 
			    (if (and (and is-waiting-for-token is-regreq)
				     (not is-regreq)) 
				(progn2 
				 (progn2 
				  (if is-q-empty exit-cs) 
				  (progn2 
				   (if-else (and want-cs is-regreq)
					    (send-token-to holder) enter-cs) 
				   (if-else (not (and want-cs is-regreq)) 
					    (if is-q-empty exit-cs) 
					    (if-else (and want-cs is-regreq)
						     (if is-q-empty exit-cs) 
						     (if (not is-regreq) enter-cs))))) 
				 (if-else (not (or is-regreq has-token)) 
					  (if is-q-empty exit-cs) 
					  (if-else (and want-cs is-regreq) 
						   (if is-q-empty exit-cs)
						   (if (not is-regreq) enter-cs))))) 
			    (if is-q-empty exit-cs)) 
			   (if is-q-empty exit-cs)))))
