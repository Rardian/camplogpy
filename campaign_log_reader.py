import json
from tag import Tag

class CampaignLogReader:
    def __init__(self, data):
        self.data = data
        #self.tags = {}
    
    def readAllTags(self):
        tags = {}

        for logEntry in self.data:
            for tagInActualTags in logEntry["actualTags"]:

                if tagInActualTags in tags:
                    tags[tagInActualTags].increaseCount()
                else:
                    tags[tagInActualTags] = Tag(tagInActualTags)
        
        def sortByTagCount(tag):
            return tag.count

        sortedValues = sorted(tags.values(), key=sortByTagCount, reverse=True)
        return sortedValues
    
    def createLinks(self, tag):
        linkedWithTag = {
            #"@Jean": {
            #    timestamp1: entry1,
            #    timestamp2: entry2
            #},
        }

        for logEntry in self.data:
            if tag.id in logEntry["actualTags"]:

                for tagInActualTags in logEntry["actualTags"]:

                    if tag.id != tagInActualTags:
                        if tagInActualTags in linkedWithTag:
                            linkedWithTag[tagInActualTags].update({logEntry["timestamp"]: logEntry["rawText"]})
                        else:
                            linkedWithTag[tagInActualTags] = {
                                #logEntry["timestamp"]: logEntry["htmlText"]
                                logEntry["timestamp"]: logEntry["rawText"]
                            }

        return linkedWithTag


