wg = Workgroup.objects.filter(name="Melbourne").first()
wg1 = Workgroup.objects.filter(name="Sydney").first()
cp = Company.objects.filter(name="Unisys").first()
cp1 = Company.objects.filter(name="Accenture").first()
cw = CompanyWorkgroup.objects.filter(company=cp, workgroup=wg).first()
cw1 = CompanyWorkgroup.objects.filter(company=cp1, workgroup=wg1).first()


http://127.0.0.1:8000/cal/?datefrom=20240108&dateto=20240114