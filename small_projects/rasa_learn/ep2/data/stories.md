## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye
  - slot{"a": true}
    - utter_greet
  - utter_cheer_up

## GOODBYE 2    
* goodbye
  - utter_goodbye
  - slot{"a": false}
    - utter_iamabot
  - utter_did_that_help
  
## bot challenge
* bot_challenge
  - utter_iamabot


## test long msg
* long
  - utter_S3.3.2.3
  - utter_S3.3.3.1
  - utter_S3.3.3.2
  - utter_S3.3.3.3
  - utter_S3.3.3.4
  - utter_S3.3.3.5
  - utter_S3.3.3.6
  - utter_S3.3.3.7
  - utter_S3.4.1
  - utter_S3.4.2
  - utter_S3.4.3
  - utter_S3.4.4
  - utter_S3.4.5
  - utter_S3.4.6
  - utter_S3.4.7
  - utter_S3.4.8


## test text slot Path 1
* S1_text
  - slot{"city": "Japan"}
  - utter_S3.3.3.1
  - utter_S3.3.3.2
  - utter_S3.3.3.3
  
  
## test text slot Path 2
* S1_text
  - slot{"city": "UA"}
  - utter_S3.3.3.3
  - utter_S3.3.3.2
  - utter_S3.3.3.1


## test categorical slot Path 1
* S2.1
- slot{"risk_level": "a"}
- utter_S3.3.3.1

## test categorical slot Path 2
* S2.1
- slot{"risk_level": "b"}
- utter_S3.3.3.2

## test categorical slot Path 3
* S2.1
- slot{"risk_level": "c"}
- utter_S3.3.3.3

## test float slot Path 1
* S2.2
- slot{"temperature": -100}
- utter_S3.3.3.1

## test float slot Path 2
* S2.2
- slot{"temperature": 100}
- utter_S3.3.3.2

## test float slot Path 3
* S2.2
- slot{"temperature": 50}
- utter_S3.3.3.3

## test list slot Path 1
* S2.3
- slot{"old_items": ["o1", "o2", 3, 4]}
- utter_S3.3.3.6

## test list slot Path 2
* S2.3
- slot{"old_items": []}
- utter_S3.3.3.7

## TEST multi conditions for story Path1
* S3.1
- slot{"risk_level": "c", "a": true}
- utter_S3.4.1


## TEST multi conditions for story Path2
* S3.1
- slot{"risk_level": "b", "a": false}
- utter_S3.4.2


## TEST multi conditions for story Path3
* S3.1
- slot{"risk_level": "b", "a": true}
- utter_S3.4.3


## TEST multi conditions for story Path4
* S3.1
- slot{"risk_level": "c", "a": false}
- utter_S3.4.4


## TEST multi line conditions for story Path1
* S3.2
- slot{"risk_level": "c"}
- utter_S3.4.4
- slot{"a": false}
- utter_S3.4.3

## TEST multi line conditions for story Path2
* S3.2
- slot{"risk_level": "b"}
- utter_S3.4.8
- slot{"a": false}
- utter_S3.4.7

## TEST multi line conditions for story Path3
* S3.2
- slot{"risk_level": "c"}
- utter_S3.4.4
- slot{"a": true}
- utter_happy

## TEST multi line conditions for story Path4
* S3.2
- slot{"risk_level": "b"}
- utter_S3.4.8
- slot{"a": true}
- utter_S3.4.5

## TEST multi float slot Path 1
* S4.1
- slot{"smoking_amount": 0.0}
- utter_S4.1

## TEST multi float slot Path 2
* S4.1
- slot{"smoking_amount": 0.1}
- utter_S4.3


## TEST multi float slot Path 3
* S4.1
- utter_S4.2


 
