# chekout https://code.visualstudio.com/docs/python/testing

import pytest
import json

import sys
sys.path.insert(0, '../')
sys.path.insert(0, 'd:/Kreativity/camplogpy')

from tag import Tag
from campaign_log_reader import CampaignLogReader

def test_readAllTags():
    with open("test/read_all_tags.json", encoding='utf-8') as f:
        # Init
        data = json.load(f)

        # Run
        allTags = CampaignLogReader(data).readAllTags()

        # Test
        expected = [
            Tag("§S01E01 Schicksalsfäden").increaseCount().increaseCount(),
            Tag("#Villerville").increaseCount(),
            Tag("@Jean Luchs"),
        ]

        assert len(allTags) == len(expected)

        index = 0
        for tag in allTags:
            assert allTags[0].id == expected[0].id, "id was " + allTags[0].id + " not " + expected[0].id
            assert allTags[0].count == expected[0].count, "count was " + allTags[0].count + " not " + expected[0].count
            index += 1

def test_createLinks():
    with open("test/create_links.json", encoding='utf-8') as f:
        # Init
        data = json.load(f)

        # Run
        linkedTags = CampaignLogReader(data).createLinks(Tag("@Jean Luchs"))

        # Test
        expected = {
            "@Eva": {
                "2018-11-02T22:33:11.131Z": "@Eva @\"Jean Luchs\" %02.10.2018 - §\"S01E01 Schicksalsfäden\""
            },
            "§S01E01 Schicksalsfäden": {
                "2018-10-02T22:33:11.131Z": "@\"Jean Luchs\" #\"Villerville\" %02.10.2018 - §\"S01E01 Schicksalsfäden\"",
                "2018-11-02T22:33:11.131Z": "@Eva @\"Jean Luchs\" %02.10.2018 - §\"S01E01 Schicksalsfäden\"",
            },
            "#Villerville": {
                "2018-10-02T22:33:11.131Z": "@\"Jean Luchs\" #\"Villerville\" %02.10.2018 - §\"S01E01 Schicksalsfäden\""
            },
        }

        assert len(linkedTags) == len(expected), "overall length is " + str(len(linkedTags)) + " not " + str(len(expected))

        for tag in linkedTags:
            linkedPosts = linkedTags[tag]
            expectedPosts = expected[tag]

            assert len(linkedPosts) == len(expectedPosts), "length of tag " + tag + " is " + str(len(linkedPosts)) + " not " + str(len(expectedPosts))

            for post in linkedPosts:
                assert linkedPosts[post] == expectedPosts[post], "post is " + linkedPosts[post] + " not " + expectedPosts[post]

if __name__ == '__main__':
    test_readAllTags()
    test_createLinks()
