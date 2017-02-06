Title: SICP Exercise 1.7
Date: 2013-02-24 17:21
Category: SICP
Tags: sicp
Authors: Wonseok Choi

원래 책에 소개된 코드는 square를 취한 결과를 x와 비교해서 적당한 값이라고
생각되면 값을 반환하게 되어있다. 1.7 문제는 이 코드를 개선하라는 것인데,
너무 작은 값이나 큰 값에 대해서 정확하게 동작하지 않기 때문이다.

floating-point 타입의 정밀도 한계때문에 아주 작은 값에 대해서 정확한 값을
얻지 못하고, 아주 큰 값에 대해서는 비효율적이거나 값을 구하지 못하게 된다.

기존 코드의 `good-enough?` procedure를 이전 추측값과 아주 근소한 차이가 나는
경우에 `#t`를 반환하도록 수정하였다. 비교 대상 값 (epsilon) 은 0.001 에서
1e-6로 바꿨다.

SICP Exercise 1.7

    :::scheme
    (define (sqrt-iter guess prev-guess x)
      (if (good-enough? guess prev-guess)
        guess
        (sqrt-iter (improve guess x)
                   guess
                   x)))
     
    (define (improve guess x)
      (average guess (/ x guess)))
     
    (define (average x y)
      (/ (+ x y) 2))
     
    (define (square x)
      (* x x))
     
    (define (good-enough? guess prev-guess)
      (< (abs (- guess prev-guess)) 1e-6))
     
    (define (sqrt x)
      (sqrt-iter 1.0 0.0 x))
     
    ;; test
    (sqrt 9)
    (sqrt (+ 100 37))
    (square (sqrt 1000))
    (sqrt 0.001)
    (sqrt 100000000000000000)

원래 코드의 결과:

    1 ]=> (sqrt 0.001)
    ;Value: .04124542607499115
    
    1 ]=> (sqrt 100000000000000000)^C
    Unhandled signal received.
    Killed by SIGQUIT.

0.001의 결과가 0.0412로 나오는데, 정밀도가 많이 떨어진다.
100000000000000000의 결과는 얻지 못하고 중지시켰다.

바꾼 코드의 결과:

    1 ]=> (sqrt 0.001)
    ;Value: .03162277660168433
    
    1 ]=> (sqrt 100000000000000000)
    ;Value: 316227766.01683795

0.001의 결과가 비교적 정확해졌고 100000000000000000의 결과도 출력하였다.
