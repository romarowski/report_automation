def replace(poll):
    poll_name =  poll.split(' (', 1)[0]
    mydict = {"₂" :"2",
              "₃" :"3",
              "₁₀":"10",
              "₅" :"5",
              }
    for key in mydict:
        poll_name = poll_name.replace(key, mydict[key])
    return poll_name
