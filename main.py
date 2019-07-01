import sys, getopt

def main(argv):
   inputfile = ''
   try:
      opts, args = getopt.getopt(argv,"i:",["ifile="])

   except getopt.GetoptError:
      print ('main.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('main.py -i <PTS input file.xlsx>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg

   print ('PTS file is ', inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])