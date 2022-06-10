from scholarship_granting_executer import ScholarshipGrantingExecuter

def main():
    sge = ScholarshipGrantingExecuter()
    sge.setupCriteria()
    sge.setupAlternativesFromFile()
    sge.obtainNormalizedDecisionMatrix()
    sge.runTOPSISMethod()
    print(sge.resultsWithThreshold)
    #sge.exportResultsWithTreshold("test1")
    #sge.exportAlternatives("test")

if __name__ == "__main__":
    main()