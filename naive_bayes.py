import csv

impact_dict = "./ImpactDict.csv"
nonimpact_dict = "./NonImpactShortDict.csv"
tweets = "./TestTweets20.csv"
res = open("./nb_results.txt", "w+")

with open(tweets) as tweets_csv:
    tweets_reader = csv.reader(tweets_csv, delimiter=',')

    for t in tweets_reader:
        impact_value = 0
        nonimpact_value = 0
        impacted = False

        for word in t:
            if word != '' and len(word) > 3:
                with open(impact_dict) as impact_csv:
                    impact_reader = csv.reader(impact_csv, delimiter=",")

                    for imp_line in impact_reader:
                        if imp_line[0] == word:
                            print(imp_line[4])
                            impact_value += float(imp_line[4])
                            break
                    #end of for
                
                with open(nonimpact_dict) as nonimpact_csv:
                    nonimpact_reader = csv.reader(nonimpact_csv, delimiter=",")

                    for nonimp_line in nonimpact_reader:
                        if nonimp_line[0] == word:
                            print(nonimp_line[4])
                            nonimpact_value += float(nonimp_line[4])
                            break
                    #end of for
        #end of for

        if impact_value > nonimpact_value:
            impacted = True
        else:
            impacted = False
        
        res.write(t[0] + ": " + str(impacted) + " -- " + str(impact_value) + " " + str(nonimpact_value) + "\n")
        print(t[0] + ": " + str(impacted))
    
    res.close()

print('END SCRIPT')

