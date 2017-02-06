Title: SICP Exercise 1.11
Date: 2013-02-24 22:18
Category: SICP
Tags: sicp
Authors: Wonseok Choi

    f(n) = n if n > 3
    f(n) = f(n-1) + 2f(n-2) + 3f(n-3) if n >= 3

f(n)을 recursive process와 iterative process로 작성하는 문제이다.

내가 기억하기로는 (책에서), 조엘 스폴스키는 C와 같은 언어를 이용해서
recursive function을 만드는 사람을 채용하지 않는다고 했는데,
stack overflow가 발생할 수 있기 때문이다.
일정한 space만 소비하는 iterative process를 구현해야만 하는 이유이다.

SICP Exercise 1.11

    :::scheme
    (define (fr n)
      (cond ((< n 3) n)
            (else (+ (fr (- n 1))
                     (* 2 (fr (- n 2)))
                     (* 3 (fr (- n 3)))))))

    (define (fi n)
      (fi-iter 0 1 2 n))
     
    (define (fi-iter a b c counter)
      (if (= counter 0)
          a
          (fi-iter b
                   c
                   (+ (* 3 a)
                      (* 2 b)
                      c)
                   (- counter 1))))
