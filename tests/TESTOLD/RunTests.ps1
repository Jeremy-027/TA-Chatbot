# tests/RunTests.ps1
# PowerShell script to run tests for the Indonesian Fashion Chatbot

# Function to display colored text
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

# Display header
Write-ColorOutput Yellow "Indonesian Fashion Chatbot - Testing Suite"
Write-Output "--------------------------------------------"

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Output "Using $pythonVersion"
}
catch {
    Write-ColorOutput Red "Error: Python is not installed or not in PATH. Please install Python and try again."
    exit 1
}

# Create the tests directory if it doesn't exist
if (-not (Test-Path -Path "tests")) {
    Write-Output "Creating tests directory..."
    New-Item -Path "tests" -ItemType Directory
    New-Item -Path "tests/__init__.py" -ItemType File
}

# Check and install required packages
Write-Output "Checking required packages..."
$requiredPackages = @("unittest", "mock", "psutil")
$missingPackages = @()

foreach ($package in $requiredPackages) {
    $packageStatus = python -c "import $package" 2>&1
    if ($LASTEXITCODE -ne 0) {
        $missingPackages += $package
    }
}

if ($missingPackages.Count -gt 0) {
    Write-ColorOutput Yellow "Installing required packages: $missingPackages"
    python -m pip install mock psutil
}

# Function to run standard unit tests
function Run-UnitTests {
    Write-ColorOutput Yellow "`nRunning Unit Tests..."
    python tests/run_all_tests.py
    return $LASTEXITCODE
}

# Function to run individual test modules
function Run-IndividualTest($moduleName) {
    Write-ColorOutput Yellow "`nRunning $moduleName tests..."
    python -m tests.$moduleName

    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput Green "$moduleName tests passed! ✓"
        return 0
    } else {
        Write-ColorOutput Red "$moduleName tests failed. ✗"
        return 1
    }
}

# Function to run performance tests
function Run-PerformanceTests {
    Write-ColorOutput Blue "`nRunning Performance Tests..."
    Write-ColorOutput Yellow "This may take a few minutes as we measure various metrics."

    $performanceTests = @("test_performance_latency", "test_resource_usage", "test_throughput", "test_speech_performance")
    $failedTests = 0

    foreach ($test in $performanceTests) {
        Write-ColorOutput Blue "`nRunning $test..."
        python -m tests.$test

        if ($LASTEXITCODE -ne 0) {
            $failedTests++
            Write-ColorOutput Red "$test failed. ✗"
        } else {
            Write-ColorOutput Green "$test completed successfully. ✓"
        }
    }

    if ($failedTests -eq 0) {
        Write-ColorOutput Green "`nAll performance tests completed successfully! ✓"
        return 0
    } else {
        Write-ColorOutput Red "`n$failedTests performance test(s) failed. See details above. ✗"
        return 1
    }
}

# Process command line arguments
$command = $args[0]

switch ($command) {
    # Run unit tests only
    "--unit" {
        Run-UnitTests
        exit $LASTEXITCODE
    }

    # Run performance tests only
    "--performance" {
        Run-PerformanceTests
        exit $LASTEXITCODE
    }

    # Run a specific test module
    "--module" {
        if ($args[1]) {
            Run-IndividualTest "test_$($args[1])"
            exit $LASTEXITCODE
        } else {
            Write-ColorOutput Red "Error: No module name provided."
            Write-Output "Usage: .\RunTests.ps1 --module MODULE_NAME"
            exit 1
        }
    }

    # Run latency tests only
    "--latency" {
        Run-IndividualTest "test_performance_latency"
        exit $LASTEXITCODE
    }

    # Run resource usage tests only
    "--resource" {
        Run-IndividualTest "test_resource_usage"
        exit $LASTEXITCODE
    }

    # Run throughput tests only
    "--throughput" {
        Run-IndividualTest "test_throughput"
        exit $LASTEXITCODE
    }

    # Run speech performance tests only
    "--speech" {
        Run-IndividualTest "test_speech_performance"
        exit $LASTEXITCODE
    }

    # Run all tests (unit + performance)
    "--all" {
        Write-ColorOutput Yellow "Running all tests (unit tests + performance tests)..."

        Run-UnitTests
        $unitStatus = $LASTEXITCODE

        Run-PerformanceTests
        $perfStatus = $LASTEXITCODE

        # Overall status
        if (($unitStatus -eq 0) -and ($perfStatus -eq 0)) {
            Write-ColorOutput Green "`nAll tests passed successfully! ✓"
            exit 0
        } else {
            Write-ColorOutput Red "`nSome tests failed. See details above. ✗"
            exit 1
        }
    }

    # Show help
    "--help" {
        Write-Output "`nUsage:"
        Write-Output "  .\RunTests.ps1                  Run unit tests (default)"
        Write-Output "  .\RunTests.ps1 --unit           Run only unit tests"
        Write-Output "  .\RunTests.ps1 --performance    Run only performance tests"
        Write-Output "  .\RunTests.ps1 --all            Run all tests (unit + performance)"
        Write-Output "  .\RunTests.ps1 --module NAME    Run tests for a specific module (without 'test_' prefix)"
        Write-Output "  .\RunTests.ps1 --latency        Run latency tests only"
        Write-Output "  .\RunTests.ps1 --resource       Run resource usage tests only"
        Write-Output "  .\RunTests.ps1 --throughput     Run throughput tests only"
        Write-Output "  .\RunTests.ps1 --speech         Run speech performance tests only"
        Write-Output "  .\RunTests.ps1 --help           Show this help message"
        Write-Output "`nAvailable test modules:"
        Write-Output "  clarification_module       Tests for parameter extraction and clarifications"
        Write-Output "  fashion_mapping            Tests for clothing recommendation mappings"
        Write-Output "  response_generator         Tests for response generation"
        Write-Output "  clothing_selector          Tests for clothing selection JSON generation"
        Write-Output "  language_model             Tests for IndoBERT model integration"
        Write-Output "  chatbot_azure              Tests for Azure speech service integration"
        Write-Output "  chatbot_interface          Tests for text-only chatbot interface"
        Write-Output "  performance_latency        Tests for response time latency"
        Write-Output "  resource_usage             Tests for memory and CPU usage"
        Write-Output "  throughput                 Tests for throughput capacity"
        Write-Output "  speech_performance         Tests for speech service performance"
        exit 0
    }

    # Default: run unit tests only
    default {
        Run-UnitTests
        exit $LASTEXITCODE
    }
}