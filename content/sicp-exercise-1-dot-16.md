Title: SICP Exercise 1.16
Date: 2013-02-24 22:50
Category: SICP
Tags: sicp
Authors: Wonseok Choi

    b^2 = b * b
    b^4 = b^2 * b^2
    b^8 = b^4 * b^4

로 부터 아래와 같은 규칙을 얻는다.

    b^n = (b^(n/2))^2 if n is even
    b^n = b * b^(n-1) if n is odd

이 것을 Big Theta (log n) growth를 갖는 procedure로 만드는 것이 1.16 문제이다.  
책에서는 recursive algorithm에 대해 설명한다
(위의 식을 그대로 옮기면 되니까 쉽게 이해됨).

이 문제는 constant space를 소비하는 iterative process를 만들라고 한다.  
`a`라는 state variable을 잘 이용하는 것이 관건이다.

SICP Exercise 1.16

    :::scheme
    ;; fast-expt linear iterative process.
    ;;
     
    (define (even? x)
      (= (remainder x 2) 0))
     
    (define (square x)
      (* x x))
     
    (define (fast-expt b n)
      (fast-expt-iter b n 1))
     
    ;; naive version
    ;;(define (fast-expt-iter b n a)
    ;;  (if (= n 0)
    ;;    a
    ;;    (fast-expt-iter b (- n 1) (* a b))))
    ;;
     
    (define (fast-expt-iter b n a)
      (if (= n 0)
        a
        (if (and (> n 0) (even? n))
          (fast-expt-iter (square b) (/ n 2) a)
          (fast-expt-iter b (- n 1) (* a b)))))
