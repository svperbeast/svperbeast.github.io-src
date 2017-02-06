Title: SICP Exercise 1.3
Date: 2013-02-24 16:59
Category: SICP
Tags: sicp
Authors: Wonseok Choi

cond 여러 개를 쭉 늘어 놓았다가, 결국 다음 코드처럼 간결하게..

    :::scheme
    (define (square x)
      (* x x))
     
    (define (sum-square-2big a b c)
      (cond ((>= a b) (+ (square a) (square (max b c))))
            (else (+ (square b) (square (max a c))))
            ))
      
    ;; test
    (if (= 0 (sum-square-2big 0 0 0)) #t #f)
    (if (= 2 (sum-square-2big -1 -1 -1)) #t #f)
    (if (= 2 (sum-square-2big 1 1 1)) #t #f)
    (if (= 13 (sum-square-2big 1 2 3)) #t #f)
    (if (= 13 (sum-square-2big 1 3 2)) #t #f)
    (if (= 13 (sum-square-2big 2 1 3)) #t #f)
    (if (= 13 (sum-square-2big 2 3 1)) #t #f)
    (if (= 13 (sum-square-2big 3 1 2)) #t #f)
    (if (= 13 (sum-square-2big 3 2 1)) #t #f)
