Anti forgery token test.

## File Structure
- `state-test.py`: This generates and check the token. 
- `templates`: html templates folder for flask, includes front page for the test

## How `state-test.py` works for anti forgery
1. Generates unique random state token when render the front page.
2. Receive information from front page with the token(1).
3. Check the token(2) if it is the same as originally generated token (3) to proceed further.

## Current issue:
At step 3 in above, token(2) and token(3) are different. Maybe for the strong cache.
I tried..
- `Chrome Developer Tools` > `Network` > ticked `Disable cache`
- `Chrome Developer Tools` > `Application` > `Clear storage` > `Clear the site data`, ticking all shown options 

A concerning is that the storage usage section (Chrome Developer Tools > Application > Clear storage) shows the following, although I haven't registered service workers. Can it cause the issue?
- 9.5KB Cache Storage
- 1.7KB Service Workers
- 1.3K IndexedDB

I'm looking for help to solve this issue. Thank you.


