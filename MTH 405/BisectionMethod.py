def bisect(f, a, b, tol=0.0000000000000000000000000001, N=200):
    p = (a+b) / 2
    FA = f(a)
    FP = f(p)
    print(f"starting values: f(a)={f(a)}, f(b)={f(b)}")
    print(f"interval: [{a}, {b}]")
    for i in range(0, N):
        p = (a+b) / 2
        FP = f(p)
        if((abs(FP) <= tol) or (b-a)/2<=tol):
            return f"Tolerance achieved, {p}, {f(p)}"
        if(FP * FA < 0):
            b = p
        else:
            a = p
            FA = FP
        print(f"interval: [{a}, {b}]")
    if(abs(FP) <= tol):
        return f"Tolerance achieved, {p}, {f(p)}"
    else:
        return f"Method failed, {p}, {f(p)}, {tol}"

def f(x):
    return (x-2)*(x-2)*(x-2)

print(bisect(f, -125, 200))