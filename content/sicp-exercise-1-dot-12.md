Title: SICP Exercise 1.12
Date: 2013-02-24 22:30
Category: SICP
Tags: sicp
Authors: Wonseok Choi

파스칼의 삼각형 문제이다.
문제 자체는 뭘 계산하라는 건지 좀 모호한데,
그냥 주어진 위치의 값을 결과로 내는 procedure를 만들었다.
위치는  (행, 열) 형식이다.

다른 사람들도 이런 식으로 생각한 것같다.

SICP Exercise 1.12

    :::scheme
    ;; Pascal's triangle
    ;;
    ;; notation: (row, column)
    ;;
    ;;   1            (1, 1)
    ;;  1 1       (2, 1)  (2, 2)
    ;; 1 2 1   (3, 1) (3, 2) (3, 3)
    ;;  ...            ...
     
    (define (pt row column)
      (cond ((= column 1) 1)
            ((= column row) 1)
            (else (+ (pt (- row 1) (- column 1))
                     (pt (- row 1) column)))))
