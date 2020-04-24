def get_gogi_phone(gogi_phone):
    if gogi_phone[1].text!='':
        return gogi_phone[1].text
    else:
        return gogi_phone[2].text
def get_gogi_work(gogi_work1,gogi_work2):
    if (len(gogi_work1) == 0):
        return gogi_work2[0].text, gogi_work2[1].text
    else:
        return gogi_work1[0].text, gogi_work2[0].text
