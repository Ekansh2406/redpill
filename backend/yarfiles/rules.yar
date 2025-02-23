rule EICAR_Test_File {
    meta:
        description = "Detects the EICAR test file used for antivirus testing"
        author = "Your Name"
        date = "2025-02-21"
    
    strings:
        $eicar_string = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

    condition:
        $eicar_string
}

