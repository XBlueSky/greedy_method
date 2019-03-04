###################################################################
# Input File example                                              #
###################################################################
# 100              Traffic inputs (MB/s)                          #(variable)
# 0.01             Ratio of the Input traffic and output traffic  #
# 5                Maximum latency (s)                            #(variable)
# 1                least error                                    #
############################    Edge   ############################
# 10000            Transmission rate of edge (MB/s)               #
# 1000             Capacity of single server (MB/s)               #
# 10               Unit cost of single server in edge             #(variable)
# 2                Maximum servers in edge                        #
############################    Fog    ############################
# 3000             Transmission rate of vehicles (MB/s)           #
# 300              Capacity of vehicles (MB/s)                    #
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