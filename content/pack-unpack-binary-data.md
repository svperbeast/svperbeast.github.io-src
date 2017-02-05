Title: Pack and Unpack Binary Data
Date: 2013-06-18 21:32
Category: Blog
Tags: struct
Slug: pack-unpack-binary-data
Authors: Wonseok Choi

Data Structure를 (파일에 저장하고) 네트워크를 통해 전송하는 수 많은 방법들이 있다.

padding없이 만든 struct, POD class 등 을 그대로 memcpy할 수도 있는데,
Endian 처리를 잘 해줘야 하며 유지보수할 때 실수를 할 가능성이 많다.

플랫폼뿐만 아니라 프로그래밍 언어 사이에서도 Data를 교환할 수 있도록 한 여러 라이브러리, 프레임워크 등 이 많다.
[protocol buffers](https://code.google.com/p/protobuf/), [thrift](http://thrift.apache.org/), [avro](http://avro.apache.org/), [MessagePack](http://msgpack.org/) 등 Data Serialization뿐 아니라 low level network I/O 및 RPC 메커니즘까지 제공하는 것들도 있다.
Go는 Go로 작성된 프로그램끼리 Data를 주고받을 수 있도록 한 [gob](http://blog.golang.org/gobs-of-data)이라는 패키지도 있다.
C++ boost 라이브러리에는 [Serialization](http://www.boost.org/doc/libs/1_53_0/libs/serialization/doc/index.html)이 있는데, [Binary format을 네트워크를 통해 잘 전송하는 것을 보장하지 않는다](http://stackoverflow.com/questions/2304061/is-it-safe-to-use-boost-serialization-to-serialize-objects-in-c-to-a-binary-fo)고 한다 (XML 등 Text 형식은 사용 가능).

이러한 라이브러리들을 사용하기 위해서, 목적에 맞는 것들을 잘 선택해야 한다.
최근에 지금 일하고 있는 회사에서 MessagePack을 사용하기로 했다
([MessagePack 및 boost asio 사용 예](http://slid.es/wonseokchoi/msgpack-asio)).

그런데, 이런 라이브러리들은 너무 _멋지다_(Fancy).
[The Practice of Programming](http://cm.bell-labs.com/cm/cs/tpop/)의 한 장에서 소개하는 Packet 처리 방식은 내게 좋은 영감을 주었다. printf의 타입을 명시하는 _little language_를 차용한 이 방식은 Erlang의 pattern matching이나 Python의 struct에서도 관찰할 수 있다고 생각한다.

Pattern matching 연산으로 IPv4 data를 파싱하는 erlang code
(Programming Erlang - Joe Armstrong):

    ...
    case Dgram of
      <<?IP_VERSION:4, HLen:4, SrvcType:8, TotLen:16,
        ID:16, Flgs:3, FragOff:13,
        TTL:8, Proto:8, HdrChkSum:16,
        SrcIP:32
        ...

Packing, Unpacking three integers
(http://docs.python.org/2/library/struct.html#examples):

    >>> from struct import *
    >>> pack('hhl', 1, 2, 3)
    '\x00\x01\x00\x02\x00\x00\x00\x03'
    >>> unpack('hhl', '\x00\x01\x00\x02\x00\x00\x00\x03')
    (1, 2, 3)

pattern matching은 규칙을 명시하는 little language의 수준을 뛰어 넘는 것으로 보인다. Python struct module의 `hhl`과 같은 문자열은 little language의 좋은 예가 된다.
The Practice of Programmig에서는 위와 같은 예를 소개하고 있다:

> 이 예는 어떤 상용 네트워크 프로토콜의 실제 코드에 기반한다.
> 필자가 일단 이 접근방식이 통할 거라고 깨닫자마자, 몇천 줄 정도 되던
> 반복적이고 에러가 생기기 쉬웠던 코드가, 유지보수하기 쉬운 몇백 줄 정도로
> 줄어들었다. 표기법이 혼란을 확 잠재운 것이다.

[struct](https://github.com/svperbeast/struct)는 Python struct module과 비슷하게 구현한 C Library이다.
이 코드에 Null-terminated string, blob data 등 을 추가한 코드는 [여기](https://github.com/Xsoda/struct)에서 확인할 수 있다.
