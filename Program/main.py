import processxml
import toproteus

def main():
    processxml.traverse(processxml.root)
    toproteus.writeProteus()

main()