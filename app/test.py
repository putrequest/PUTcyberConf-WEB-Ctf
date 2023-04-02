import jwt

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWnEmSI6IlJvYmVydCBXaXRvbGQgTWFrxYJvd2ljeiIsImRhdGFfdXJvZHplbmlhIjoiMTIuMDcuMTk2MyIsImZ1bmtjamEiOiJ3acSZemllxYQiLCJrb3BlcmVrIjowfQ.tTCKnVHCU42ch7XFMes9dcIKUZPgfoNcTivvCxQFAYk'
token_bytes = token.encode('ascii')
decodedJWT = jwt.decode(token, '832p13c2ny_k1uc2', algorithms=['HS256'])
print(decodedJWT["funkcja"])
