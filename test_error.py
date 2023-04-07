import ROOT
import random

# Create histograms to keep track of events
h_pass = ROOT.TH1D("h_pass", "h_pass", 10, 0.5, 10.5)
h_total = ROOT.TH1D("h_total", "h_total", 10, 0.5, 10.5)
h_fail = ROOT.TH1D("h_fail", "h_fail", 10, 0.5, 10.5)

# Enable sum of squares calculation for histogram errors
h_pass.Sumw2()
h_total.Sumw2()
h_fail.Sumw2()

# Generate events and fill histograms
for i in range(1, h_pass.GetNbinsX()+1):
    # Generate a random number of events between 100 and 1000
    n = random.uniform(100, 1000)
    for j in range(int(n)):
        # Generate a weight for the event
        w = random.gauss(1, 0.1)
        # Determine if event passes or fails
        r = random.uniform(0, 1)
        if r < 0.2:
            h_pass.Fill(i, w)
        else:
            h_fail.Fill(i, w)
        # Add event to total histogram
        h_total.Fill(i, w)

# Calculate efficiency using default TEfficiency method
print("===== default TEfficiencty =====")
eff = ROOT.TEfficiency(h_pass, h_total)
for i in range(1, h_pass.GetNbinsX()+1):
    # Get efficiency and errors for each bin
    print(f"Bin {i-1}: {eff.GetEfficiency(i):.4f} + {eff.GetEfficiencyErrorUp(i):.4f} - {eff.GetEfficiencyErrorLow(i):.4f}")

# Calculate efficiency using TH1::Divide method
print("===== default TH1::Divide =====")
h_eff = h_pass.Clone("h_eff")
h_eff.Divide(h_total)
for i in range(1, h_pass.GetNbinsX()+1):
    # Get efficiency and errors for each bin
    print(f"Bin {i-1}: {h_eff.GetBinContent(i):.4f} + {h_eff.GetBinError(i):.4f} - {h_eff.GetBinError(i):.4f}")

# Calculate efficiency and errors manually
print("===== calculate error by hand =====")
for i in range(1, h_pass.GetNbinsX()+1):
    # Get values and errors for pass and fail histograms
    p = h_pass.GetBinContent(i)
    f = h_fail.GetBinContent(i)
    p_err = h_pass.GetBinError(i)
    f_err = h_fail.GetBinError(i)
    # Calculate efficiency and error using formulas
    eff = p / (p + f)
    eff_err = (f*f*p_err*p_err + p*p*f_err*f_err)**0.5 / (p + f)**2
    # Print results
    print(f"Bin {i-1}: {eff:.4f} + {eff_err:.4f} - {eff_err:.4f}")
