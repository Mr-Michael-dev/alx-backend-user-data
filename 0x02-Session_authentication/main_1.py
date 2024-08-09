#!/usr/bin/python3
""" Check response
"""

if __name__ == "__main__":

    try:
        from api.v1.auth.session_auth import SessionAuth
        sa = SessionAuth()
        user_id_1 = "User 1"
        session_id_1 = sa.create_session(user_id_1)
        if session_id_1 is None:
            print("create_session doesn't return a session ID when user_id is a string")
            exit(1)
        if sa.user_id_by_session_id is None:
            print("user_id_by_session_id should not be None")
            exit(1)
        if type(sa.user_id_by_session_id) is not dict:
            print("user_id_by_session_id should be a dictionary: {}".format(sa.user_id_by_session_id))
            exit(1)
        r_user_id_1 = sa.user_id_by_session_id.get(session_id_1)
        if r_user_id_1 != user_id_1:
            print("User doesn't found for this session ID: {} -> {}".format(session_id_1, sa.user_id_by_session_id))
            exit(1)

        user_id_2 = "User 1"
        session_id_2 = sa.create_session(user_id_2)
        if session_id_2 is None:
            print("create_session doesn't return a session ID when user_id is a string")
            exit(1)
        if sa.user_id_by_session_id is None:
            print("user_id_by_session_id should not be None")
            exit(1)
        if type(sa.user_id_by_session_id) is not dict:
            print("user_id_by_session_id should be a dictionary: {}".format(sa.user_id_by_session_id))
            exit(1)
        r_user_id_2 = sa.user_id_by_session_id.get(session_id_2)
        if r_user_id_2 != user_id_2:
            print("User doesn't found for this session ID: {} -> {}".format(session_id_2, sa.user_id_by_session_id))
            exit(1)
        
        if session_id_1 == session_id_2:
            print("Same User should not have the same session ID if we create twice a session: {}".format(sa.user_id_by_session_id))
            exit(1)
        print("OK", end="")
    except:
        import sys
        print("Error: {}".format(sys.exc_info()))