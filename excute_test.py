__author__ = 'liziqiang'


print "outside of func!"


def f():
    print "inside f()!"


def main(a, b, c):
    import sys
    print a,b,c
    print sys.argv
    print "inside main()!"
    f()


if __name__ =='__main__':
    main(1, 2, 3)