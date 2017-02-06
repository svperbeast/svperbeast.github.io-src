Title: SICP Exercise 1.8
Date: 2013-02-24 22:03
Category: SICP
Tags: sicp
Authors: Wonseok Choi

세 제곱근을 구하는 문제다.
exercise 1.7의 `improve` procedure만 바꿔주면 된다.

SICP Exercise 1.8

    :::scheme
    (define (cuberoot-iter guess prev-guess x)
      (if (good-enough? guess prev-guess)
        guess
        (cuberoot-iter (improve guess x) guess x)))
     
    (define (improve guess x)
      (/ (+ (/ x (square guess))
            (* 2 guess))
         3))
     
    (define (square x)
      (* x x))
     
    (define (cube x)
      (* x x x))
     
    (define (good-enough? guess prev-guess)
      (< (abs (- guess prev-guess)) 1e-6))
     
    (define (cuberoot x)
      (cuberoot-iter 1.0 0.0 x))
     
    ;; test
    (cuberoot 27)
    (cube (cuberoot 1000))
    (cuberoot 0.001)
    (cuberoot 100000000000000000)

결과:

    1 ]=> ;; test
    (cuberoot 27)
    ;Value: 3.0000000000000977

    1 ]=> (cube (cuberoot 1000))
    ;Value: 1000.0000000000005

    1 ]=> (cuberoot 0.001)
    ;Value: .10000000000000005

    1 ]=> (cuberoot 100000000000000000)
    ;Value: 464158.88336127787
