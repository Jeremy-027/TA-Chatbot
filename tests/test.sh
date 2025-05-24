#!/bin/bash
# test.sh - Run all tests for the Indonesian Fashion Chatbot

# Set colors for better terminal output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Indonesian Fashion Chatbot - Testing Suite${NC}"
echo "--------------------------------------------"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Create the tests directory if it doesn't exist
if [ ! -d "tests" ]; then
    echo "Creating tests directory..."
    mkdir -p tests
    touch tests/__init__.py
fi

# Check if required packages are installed
echo "Checking required packages..."
REQUIRED_PACKAGES="unittest mock psutil concurrent.futures statistics"
MISSING_PACKAGES=""

for package in $REQUIRED_PACKAGES; do
    python3 -c "import $package" 2>/dev/null
    if [ $? -ne 0 ]; then
        MISSING_PACKAGES="$MISSING_PACKAGES $package"
    fi
done

if [ ! -z "$MISSING_PACKAGES" ]; then
    echo -e "${YELLOW}Installing required packages: $MISSING_PACKAGES ${NC}"
    pip install mock psutil
fi

# Function to run standard unit tests
run_unit_tests() {
    echo -e "\n${YELLOW}Running Unit Tests...${NC}"
    python3 tests/run_all_tests.py
    return $?
}

# Function to run individual test modules
run_individual_test() {
    echo -e "\n${YELLOW}Running $1 tests...${NC}"
    python3 -m tests.$1

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}$1 tests passed! ✓${NC}"
        return 0
    else
        echo -e "${RED}$1 tests failed. ✗${NC}"
        return 1
    fi
}

# Function to run performance tests
run_performance_tests() {
    echo -e "\n${BLUE}Running Performance Tests...${NC}"
    echo -e "${YELLOW}This may take a few minutes as we measure various metrics.${NC}"

    PERFORMANCE_TESTS=("test_performance_latency" "test_resource_usage" "test_throughput" "test_speech_performance")
    FAILED_TESTS=0

    for test in "${PERFORMANCE_TESTS[@]}"; do
        echo -e "\n${BLUE}Running $test...${NC}"
        python3 -m tests.$test

        if [ $? -ne 0 ]; then
            FAILED_TESTS=$((FAILED_TESTS+1))
            echo -e "${RED}$test failed. ✗${NC}"
        else
            echo -e "${GREEN}$test completed successfully. ✓${NC}"
        fi
    done

    if [ $FAILED_TESTS -eq 0 ]; then
        echo -e "\n${GREEN}All performance tests completed successfully! ✓${NC}"
        return 0
    else
        echo -e "\n${RED}$FAILED_TESTS performance test(s) failed. See details above. ✗${NC}"
        return 1
    fi
}

# Process command line arguments
case "$1" in
    # Run unit tests only
    "--unit")
        run_unit_tests
        exit $?
        ;;

    # Run performance tests only
    "--performance")
        run_performance_tests
        exit $?
        ;;

    # Run a specific test module
    "--module")
        if [ -n "$2" ]; then
            run_individual_test "test_$2"
            exit $?
        else
            echo -e "${RED}Error: No module name provided.${NC}"
            echo "Usage: ./test.sh --module MODULE_NAME"
            exit 1
        fi
        ;;

    # Run latency tests only
    "--latency")
        run_individual_test "test_performance_latency"
        exit $?
        ;;

    # Run resource usage tests only
    "--resource")
        run_individual_test "test_resource_usage"
        exit $?
        ;;

    # Run throughput tests only
    "--throughput")
        run_individual_test "test_throughput"
        exit $?
        ;;

    # Run speech performance tests only
    "--speech")
        run_individual_test "test_speech_performance"
        exit $?
        ;;

    # Run all tests (unit + performance)
    "--all")
        echo -e "${YELLOW}Running all tests (unit tests + performance tests)...${NC}"

        run_unit_tests
        UNIT_STATUS=$?

        run_performance_tests
        PERF_STATUS=$?

        # Overall status
        if [ $UNIT_STATUS -eq 0 ] && [ $PERF_STATUS -eq 0 ]; then
            echo -e "\n${GREEN}All tests passed successfully! ✓${NC}"
            exit 0
        else
            echo -e "\n${RED}Some tests failed. See details above. ✗${NC}"
            exit 1
        fi
        ;;

    # Show help
    "--help")
        echo -e "\nUsage:"
        echo -e "  ./test.sh                  Run unit tests (default)"
        echo -e "  ./test.sh --unit           Run only unit tests"
        echo -e "  ./test.sh --performance    Run only performance tests"
        echo -e "  ./test.sh --all            Run all tests (unit + performance)"
        echo -e "  ./test.sh --module NAME    Run tests for a specific module (without 'test_' prefix)"
        echo -e "  ./test.sh --latency        Run latency tests only"
        echo -e "  ./test.sh --resource       Run resource usage tests only"
        echo -e "  ./test.sh --throughput     Run throughput tests only"
        echo -e "  ./test.sh --speech         Run speech performance tests only"
        echo -e "  ./test.sh --help           Show this help message"
        echo -e "\nAvailable test modules:"
        echo -e "  clarification_module       Tests for parameter extraction and clarifications"
        echo -e "  fashion_mapping            Tests for clothing recommendation mappings"
        echo -e "  response_generator         Tests for response generation"
        echo -e "  clothing_selector          Tests for clothing selection JSON generation"
        echo -e "  language_model             Tests for IndoBERT model integration"
        echo -e "  chatbot_azure              Tests for Azure speech service integration"
        echo -e "  chatbot_interface          Tests for text-only chatbot interface"
        echo -e "  performance_latency        Tests for response time latency"
        echo -e "  resource_usage             Tests for memory and CPU usage"
        echo -e "  throughput                 Tests for throughput capacity"
        echo -e "  speech_performance         Tests for speech service performance"
        exit 0
        ;;

    # Default: run unit tests only
    *)
        run_unit_tests
        exit $?
        ;;
esac