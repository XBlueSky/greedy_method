###################################################################
# Input File example                                              #
###################################################################
# 3000             Traffic inputs (MB/s)                          #(variable)
# 0.01             Ratio of the Input traffic and output traffic  #
# 0.001 (1 ms)     Maximum latency (s)                            #(variable)
# 1                least error                                    #
############################    Edge   ############################
# 1250  (10 Gbps)  Transmission rate of edge (MB/s)               #
# 20               Capacity of single server (MB/s)               #
# 20               Unit cost of single server in edge             #
# 10               Maximum servers in edge                        #
############################    Fog    ############################
# 1250  (10 Gbps)  Transmission rate of vehicles (MB/s)           #
# 5                Capacity of each vehicle (MB/s)                #
# 2                Number of fogs                                 #
# 3 5              Number of vehicles in fog                      #
############################   Fog 1   ############################
# 20 20 20         Unit cost of vehicle                           #
# 2  2  2          % of power consumption rate                    #
# 50 70 55         % of initial power of vehicle                  #
# 20 10 50         % of threshold power vehicle                   #
############################   Fog 2   ############################
# 20 20 20 20 20   Unit cost of vehicle                           #
# 2  2  2  2  2    % of power consumption rate                    #
# 21 20 50 45 80   % of initial power of vehicle                  #
# 20 10 10 40 20   % of threshold power of vehicle                #
###################################################################