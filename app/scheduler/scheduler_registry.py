from scheduler.printHelloScheduler import printHelloScheduler

"""
    SCHEDULER_REGISTRY
    주기적으로 실행될 함수의 목록을 관리합니다.
    함수의 목록은 다음과 같은 리스트로 정의됩니다.

        [ 함수, 주기(정수형, 초 단위) ]

    ex 
    [ printHelloScheduler , 5] 
    => 5초에 한 번씩 printHelloScheduler가 실행됨
"""
SCHEDULER_REGISTRY = [
    # [printHelloScheduler, 5],
]