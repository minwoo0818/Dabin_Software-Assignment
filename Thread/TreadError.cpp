#include <iostream>
#include <thread>
#include <vector>

using namespace std;

const int THREADS = 2;        
const int NUM = 1000000;    

int counter = 0; 



void Counter() {
    for (int i = 0; i < NUM; i++) {
        counter++;
    }
}

void Counter1() {
    for (int i = NUM; i > 0; i--) {
        counter--;
    }
}

int main() {
    vector<thread> threads; 

    for (int i = 0; i < 1; i++) {
        threads.push_back(thread(Counter));
    }
    
     for (int i = 0; i < 1; i++) {
        threads.push_back(thread(Counter1));
    }

    for (auto &th : threads) {
        th.join();
    }

    cout << "최종 counter 값 : " << counter << endl;
    cout << "예상 counter 값 : " << 0 << endl;

    return 0;
}
