def replace(poll):
    poll_name =  poll.split(' (', 1)[0]
    mydict = {"₂" :"two",
              "₃" :"three",
              "₁₀":"ten",
              "₅" :"five",
              "." :""}
    for key in mydict:
        poll_name = poll_name.replace(key, mydict[key])
    return poll_name
