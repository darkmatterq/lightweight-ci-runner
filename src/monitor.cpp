#include<iostream>
#include<fstream>
#include<string>
#include<filesystem>
#include<chrono>
#include<thread>
#include<csignal>
#include<atomic>
const std::string COLOR_RESET ="\033[0m";
const std::string COLOR_GREEN ="\033[32m";
const std::string COLOR_YELLOW ="\033[33m";
const std::string COLOR_RED ="\033[31m";
const std::string COLOR_CYAN ="\033[36m";
const std::string COLOR_BOLD ="\033[1m";
std::string get_cpu_color(double cpu_percent){
    if(cpu_percent <50.0)
    return COLOR_GREEN;
    if(cpu_percent<80.0)
    return COLOR_YELLOW;
    return COLOR_RED;

}

std::string find_cgroup_path(const std::string& container_id){
    std::string directory_main="/sys/fs/cgroup/system.slice/docker-"+container_id+".scope";
    if (!std::filesystem::exists(directory_main))
    {   std::string pdir="/sys/fs/cgroup/system.slice";
        if(!std::filesystem::exists(pdir)){
            std::cerr <<"Cannot find cgroup directory for container: "<< container_id <<"\n";
            return "";
        }
        std::string directory="docker-"+container_id;
        for (const auto& entry: std::filesystem::directory_iterator(pdir)){
            std::string sample=entry.path().filename().string();
            if (sample.find(directory)==0)
            {
                return entry.path().string();
            }
        }
    }
    return directory_main;
}
double get_memory_usage_mb(const std::string& cgroup_path){
    std::string mem_path=cgroup_path+"/memory.current";
    std::ifstream file(mem_path);
    if(!file.is_open()){
        return -1;
    }
    double ram;
    file >> ram;
    file.close();
    return ram/(1024.0*1024.0);
}
uint64_t get_cpu_usec(const std::string& cgroup_path){
    std::string cpu_path=cgroup_path+"/cpu.stat";
    std::ifstream file(cpu_path);
    if(!file.is_open()){
        return 0;
    }
    std::string key;
    uint64_t value;
    while(file>>key>>value){
        if (key=="usage_usec"){
            return value;
        }
    }
    return 0;
}

std::atomic<bool> keep_running(true);
void handle_signal(int /*signal*/){
    keep_running=false;
}
int main(int argc, char* argv[]){
    if(argc<2){
        std::cerr<<"You have filled it out incorrectly. Please fill it out again.\n";
        std::cerr<<"Usage: ./bin/ci-monitor <container_id>\n";
        std::cerr<<"Example: ./bin/ci-monitor 7f8a9b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f90\n";
        return 1;
    }
    std::string container_id= argv[1];
    int interval_ms=500;
    if(argc>=3){
        interval_ms=std::stoi(argv[2]);
    }
    std:: cout<<"Monitoring container: "<< container_id<< 
    "\n";
    std:: cout<<"Interval: "<< interval_ms << "ms\n";
    std::signal(SIGINT, handle_signal);
    std:: signal(SIGTERM, handle_signal);
    std::string cgroup_path=find_cgroup_path(argv[1]);
    if(cgroup_path.empty()){
        std::cerr <<"Cannot find cgroup directory for container: "<< container_id <<"\n";
        return 1;
    }
    uint64_t prev_cpu_usec = get_cpu_usec(cgroup_path);
    auto prev_time =std::chrono::steady_clock::now();
    double max_cpu_usec = 0;
    double max_ram = 0;
    auto start_time = prev_time;
    while(keep_running)
    {
        std::this_thread::sleep_for(std::chrono::milliseconds(interval_ms));
        double ram_mb=get_memory_usage_mb(cgroup_path);
        if(ram_mb<0){
            std::cout<<"\n"<<COLOR_CYAN<< "[CI-MONITOR]"<< COLOR_RESET<<"Container finished. Stopping monitor.\n";
            break;
        }
        if ( max_ram < ram_mb)
        {
            max_ram=ram_mb;
        }
        uint64_t curr_cpu_usec= get_cpu_usec(cgroup_path);
        auto curr_time=std::chrono::steady_clock::now();
        int64_t delta_time_usec=std::chrono::duration_cast<std::chrono::microseconds>(curr_time-prev_time).count();
        int64_t delta_cpu_usec=curr_cpu_usec-prev_cpu_usec;
        double cpu_percent=0.0;
        if (delta_time_usec>0 && delta_cpu_usec>=0){
            cpu_percent=(static_cast<double>(delta_cpu_usec)/delta_time_usec)*100.0;
        }
        if ( max_cpu_usec < cpu_percent)
        {
            max_cpu_usec = cpu_percent;
        }
        prev_cpu_usec=curr_cpu_usec;
        prev_time=curr_time;
        std::string cpu_color= get_cpu_color(cpu_percent);
        std::cout<< COLOR_CYAN <<"[CI-MONITOR]"<<COLOR_RESET 
        << "RAM: "<< COLOR_BOLD << ram_mb <<" MB"<< COLOR_RESET
        << " | CPU: "<< cpu_color<< cpu_percent << "%"<< COLOR_RESET<<"\n";
}
    auto last_time=std::chrono::steady_clock::now();
    auto duration= last_time-start_time;
    auto duration_in_sec = std::chrono::duration_cast<std::chrono::seconds>(duration);
    std::cout<<"----------------------------------------------------------------\n";
    std::cout<<COLOR_CYAN<<" [CI-MONITOR SUMMARY]"<<COLOR_RESET<<"\n";
    std::cout<<" Peak CPU Usage : "<<get_cpu_color(max_cpu_usec)<<max_cpu_usec
    <<"%"<<COLOR_RESET<<"\n";
    std::cout<<" Peak RAM Usage : "<<max_ram<<"MB\n";
    std::cout<<" Duration       : "<< duration_in_sec.count() << " seconds\n";
    std::cout<<"----------------------------------------------------------------";
    std::cout<< "\n Monitor stopped cleanly.\n";
    return 0;
}
