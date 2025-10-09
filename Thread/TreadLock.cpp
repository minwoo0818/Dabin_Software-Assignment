#include <iostream>
#include <thread>
#include <vector>
#include <mutex> 

int counter = 0;
const int THREADS = 2;
const int NUM = 1000000;

std::mutex mtx; 

void Counter() {
    for (int i = 0; i < NUM; i++) {
        std::lock_guard<std::mutex> lock(mtx); 
        counter++;
    }
}
void Counter1() {
    for (int i = 0; i < NUM; i++) {
        std::lock_guard<std::mutex> lock(mtx); 
        counter--;
    }
}

int main() {
    std::vector<std::thread> threads; 

    for (int i = 0; i < THREADS; i++) {
        threads.push_back(std::thread(Counter));
        threads.push_back(std::thread(Counter1));
    }

    for (auto &th : threads) {
        th.join();
    }

    std::cout << "최종 counter 값 : " << counter << std::endl;
    std::cout << "예상 counter 값 : " << 0 << std::endl;

    return 0;
}