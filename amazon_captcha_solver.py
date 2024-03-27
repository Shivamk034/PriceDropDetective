from amazoncaptcha import AmazonCaptcha

solution = AmazonCaptcha('cap.png').solve()

if(solution=="Not solved"):
    pass
else:
    print(solution)