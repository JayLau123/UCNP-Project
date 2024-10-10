#ifndef TM_ADJUSTABLE_PARAMETER_HPP
#define TM_ADJUSTABLE_PARAMETER_HPP

class TmAdjustableParameter {
public:
    // Refractive index
    static constexpr double n = 1.5;

    // Overlap integral
    static constexpr double s0 = 0.00014;

    // Multi phonon
    static constexpr int n_phonon = 10;

    // Max phonon energy of NaYF4
    static constexpr double E_phonon = 450.0;

    // Zero-phonon relaxation rate
    static constexpr double W0 = 2e7;

    // MPR rate constant
    static constexpr double alpha = 3.5e-3;

    // Phonon correction factor in ED
    static constexpr double beta = 2e-3;

    // Nanoparticle diameter: 8 nm
    static constexpr double d = 8.0;

    // No shell
    static constexpr bool shell = false;

    // Critical distance: 1 nm
    static constexpr double r0 = 1.0;

    // ET constant
    static constexpr double ET_constant = (8 * 3.14 * 3.14 * (4.8e-10) * (4.8e-10) * (4.8e-10) * (4.8e-10)) / 
                                           (3 * (6.626e-27) * (6.626e-27) * 3e10);
    
    // ET threshold
    static constexpr double threshold = 1e-42;
};

#endif // TM_ADJUSTABLE_PARAMETER_HPP