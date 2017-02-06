Title: SICP Exercise 1.6
Date: 2013-02-24 17:09
Category: SICP
Tags: sicp
Authors: Wonseok Choi

SICP (Structure and Interpretation of Computer Programs)를 공부하는 사람이 꽤
많은 듯 하다. 관련 블로그도 많고, 다 볼 수 있을지 모르겠지만,
How To Design Programs 살 때 덤으로 산건데 이걸 먼저 보고 있다..

아무튼 Exercise 1.6 은 `cond` 를 이용해 `if` 를 대체하는 procedure를 만들어
사용하면 어떻게 되느냐 이다. 책의 앞에서 다루었던
applicative-order evaluation과 관련이 있는데,
내가 사용하는 mit-scheme에서는 다음과 같은 메시지가 출력된다.

    ;Aborting!: maximum recursion depth exceeded

_procedure의 인자들이 평가되는데, `sqrt-iter`의 `else-clause`에서
`sqrt-iter`를 호출하기 때문에 무한 루프에 빠지게 된다._

SICP Exercise 1.6

    :::scheme
    (define (new-if predicate then-clause else-clause)
      (cond (predicate then-clause)
            (else else-clause)))
     
    (define (sqrt-iter guess x)
      (new-if (good-enough? guess x)
        guess
        (sqrt-iter (improve guess x)
                   x)))
      
    (define (improve guess x)
      (average guess (/ x guess)))
       
    (define (average x y)
      (/ (+ x y) 2))
        
    (define (square x)
      (* x x))
         
    (define (good-enough? guess x)
      (< (abs (- (square guess) x)) 0.001))
          
    (define (sqrt x)
      (sqrt-iter 1.0 x))
