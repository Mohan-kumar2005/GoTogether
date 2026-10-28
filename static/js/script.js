

document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    // ---------- Navbar Scroll Effect ----------

    const navbar = document.querySelector(".navbar-gotogether");

    function updateNavbar() {
        if (!navbar) return;

        if (window.scrollY > 20) {
            navbar.classList.add("navbar-scrolled");
        } else {
            navbar.classList.remove("navbar-scrolled");
        }
    }

    updateNavbar();

    window.addEventListener("scroll", updateNavbar, {
        passive: true
    });


    // ---------- Highlight Current Navigation Link ----------

    const currentPath = window.location.pathname;

    document.querySelectorAll(
        ".navbar-gotogether .navbar-nav .nav-link"
    ).forEach(function (link) {
        const href = link.getAttribute("href");

        if (!href) return;

        try {
            const linkUrl = new URL(href, window.location.origin);

            if (
                linkUrl.origin === window.location.origin &&
                linkUrl.pathname === currentPath
            ) {
                link.classList.add("active");
                link.setAttribute("aria-current", "page");
            }
        } catch (error) {
            // Ignore invalid navigation URLs.
        }
    });


    // ---------- Mobile Navigation Auto-Close ----------

    const navbarCollapse = document.getElementById("navbarContent");

    if (navbarCollapse && window.bootstrap) {
        const mobileNavLinks = navbarCollapse.querySelectorAll(
            ".navbar-nav .nav-link"
        );

        mobileNavLinks.forEach(function (link) {
            link.addEventListener("click", function () {
                if (
                    window.innerWidth < 992 &&
                    navbarCollapse.classList.contains("show")
                ) {
                    const collapseInstance =
                        bootstrap.Collapse.getOrCreateInstance(
                            navbarCollapse,
                            { toggle: false }
                        );

                    collapseInstance.hide();
                }
            });
        });
    }


    // ---------- Django Alert Close Animation ----------

    document.querySelectorAll(".gt-alert").forEach(function (alert) {
        alert.addEventListener("closed.bs.alert", function () {
            alert.remove();
        });
    });


    // ---------- Profile Dropdown Accessibility ----------

    document.querySelectorAll(".profile-toggle").forEach(function (button) {
        button.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                button.blur();
            }
        });
    });


    // ---------- Footer Current Year ----------

    // Optional: automatically update the copyright year.
    // Add id="copyright-year" to a year element if desired.

    const copyrightYear = document.getElementById("copyright-year");

    if (copyrightYear) {
        copyrightYear.textContent = new Date().getFullYear();
    }

});

/* ==========================================
   GoTogether — Shared JavaScript
   File: static/js/script.js
   ========================================== */

document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    // Navbar scroll effect
    const navbar = document.querySelector(".navbar-gotogether");

    function updateNavbar() {
        if (!navbar) return;

        navbar.classList.toggle(
            "navbar-scrolled",
            window.scrollY > 20
        );
    }

    updateNavbar();

    window.addEventListener("scroll", updateNavbar, {
        passive: true
    });

    // Highlight the current navigation page
    const currentPath = window.location.pathname;

    document.querySelectorAll(
        ".navbar-gotogether .navbar-nav .nav-link"
    ).forEach(function (link) {
        const href = link.getAttribute("href");

        if (!href) return;

        try {
            const url = new URL(href, window.location.origin);

            if (
                url.origin === window.location.origin &&
                url.pathname === currentPath
            ) {
                link.classList.add("active");
                link.setAttribute("aria-current", "page");
            }
        } catch (error) {
            // Ignore invalid links.
        }
    });

    // Close the mobile navbar after clicking a navigation link
    const navbarContent = document.getElementById("navbarContent");

    if (navbarContent && window.bootstrap) {
        navbarContent.querySelectorAll(".navbar-nav .nav-link")
            .forEach(function (link) {
                link.addEventListener("click", function () {
                    if (
                        window.innerWidth < 992 &&
                        navbarContent.classList.contains("show")
                    ) {
                        bootstrap.Collapse
                            .getOrCreateInstance(navbarContent, {
                                toggle: false
                            })
                            .hide();
                    }
                });
            });
    }

    // Auto-dismiss Django alerts after 6 seconds
    document.querySelectorAll(".gt-alert").forEach(function (alert) {
        window.setTimeout(function () {
            if (
                alert.isConnected &&
                window.bootstrap &&
                !alert.classList.contains("d-none")
            ) {
                const instance = bootstrap.Alert.getOrCreateInstance(alert);
                instance.close();
            }
        }, 6000);
    });

    // Prevent choosing a past travel date in the homepage search form
    const travelDate = document.getElementById("travel-date");

    if (travelDate) {
        const now = new Date();
        const localDate = [
            now.getFullYear(),
            String(now.getMonth() + 1).padStart(2, "0"),
            String(now.getDate()).padStart(2, "0")
        ].join("-");

        travelDate.min = localDate;
    }

});

/* =========================================
   GOTogether CONTACT PAGE JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contactForm");
    const contactPhone = document.getElementById("contactPhone");
    const contactMessage = document.getElementById("contactMessage");
    const messageCount = document.getElementById("messageCount");
    const contactSubmit = document.getElementById("contactSubmit");

    // Stop if the current page does not contain the contact form.
    if (!contactForm) {
        return;
    }

    // -------------------------------------
    // MESSAGE CHARACTER COUNTER
    // -------------------------------------

    function updateMessageCount() {
        if (!contactMessage || !messageCount) {
            return;
        }

        messageCount.textContent = contactMessage.value.length;
    }

    if (contactMessage) {
        contactMessage.addEventListener("input", updateMessageCount);
        updateMessageCount();
    }

    // -------------------------------------
    // PHONE NUMBER VALIDATION
    // -------------------------------------

    if (contactPhone) {
        contactPhone.addEventListener("input", function () {
            contactPhone.setCustomValidity("");
        });

        contactPhone.addEventListener("blur", function () {
            const phone = contactPhone.value.trim();

            // Phone number is optional.
            if (phone === "") {
                contactPhone.setCustomValidity("");
                return;
            }

            const validCharacters = /^[0-9+() -]+$/.test(phone);
            const digitCount = phone.replace(/\D/g, "").length;

            if (!validCharacters || digitCount < 7 || digitCount > 15) {
                contactPhone.setCustomValidity(
                    "Enter a valid phone number containing 7 to 15 digits."
                );
            } else {
                contactPhone.setCustomValidity("");
            }
        });
    }

    // -------------------------------------
    // FORM SUBMISSION
    // -------------------------------------

    contactForm.addEventListener("submit", function (event) {
        // Allow the browser to display native validation errors.
        if (!contactForm.checkValidity()) {
            event.preventDefault();
            contactForm.reportValidity();
            return;
        }

        const message = contactMessage
            ? contactMessage.value.trim()
            : "";

        if (!message) {
            event.preventDefault();

            if (contactMessage) {
                contactMessage.setCustomValidity(
                    "Please enter your message."
                );
                contactMessage.reportValidity();
            }

            return;
        }

        if (contactMessage) {
            contactMessage.setCustomValidity("");
        }

        // Prevent accidental double-click submissions.
        if (contactSubmit) {
            contactSubmit.disabled = true;

            const label = contactSubmit.querySelector(".submit-label");

            if (label) {
                label.textContent = "Sending message...";
            }
        }

        // The browser submits the form to Django normally.
        // Django should validate and save the message server-side.
    });
});

/* =========================================
   GOTogether CONTACT PAGE JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    const contactForm = document.getElementById("contactForm");
    const contactPhone = document.getElementById("contactPhone");
    const contactMessage = document.getElementById("contactMessage");
    const messageCount = document.getElementById("messageCount");
    const contactSubmit = document.getElementById("contactSubmit");

    // Stop if the current page does not contain the contact form.
    if (!contactForm) {
        return;
    }

    // -------------------------------------
    // MESSAGE CHARACTER COUNTER
    // -------------------------------------

    function updateMessageCount() {
        if (!contactMessage || !messageCount) {
            return;
        }

        messageCount.textContent = contactMessage.value.length;
    }

    if (contactMessage) {
        contactMessage.addEventListener("input", updateMessageCount);
        updateMessageCount();
    }

    // -------------------------------------
    // PHONE NUMBER VALIDATION
    // -------------------------------------

    if (contactPhone) {
        contactPhone.addEventListener("input", function () {
            contactPhone.setCustomValidity("");
        });

        contactPhone.addEventListener("blur", function () {
            const phone = contactPhone.value.trim();

            // Phone number is optional.
            if (phone === "") {
                contactPhone.setCustomValidity("");
                return;
            }

            const validCharacters = /^[0-9+() -]+$/.test(phone);
            const digitCount = phone.replace(/\D/g, "").length;

            if (!validCharacters || digitCount < 7 || digitCount > 15) {
                contactPhone.setCustomValidity(
                    "Enter a valid phone number containing 7 to 15 digits."
                );
            } else {
                contactPhone.setCustomValidity("");
            }
        });
    }

    // -------------------------------------
    // FORM SUBMISSION
    // -------------------------------------

    contactForm.addEventListener("submit", function (event) {
        // Allow the browser to display native validation errors.
        if (!contactForm.checkValidity()) {
            event.preventDefault();
            contactForm.reportValidity();
            return;
        }

        const message = contactMessage
            ? contactMessage.value.trim()
            : "";

        if (!message) {
            event.preventDefault();

            if (contactMessage) {
                contactMessage.setCustomValidity(
                    "Please enter your message."
                );
                contactMessage.reportValidity();
            }

            return;
        }

        if (contactMessage) {
            contactMessage.setCustomValidity("");
        }

        // Prevent accidental double-click submissions.
        if (contactSubmit) {
            contactSubmit.disabled = true;

            const label = contactSubmit.querySelector(".submit-label");

            if (label) {
                label.textContent = "Sending message...";
            }
        }

        // The browser submits the form to Django normally.
        // Django should validate and save the message server-side.
    });
});

/* =========================================
   GOTogether SIGNUP & OTP JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    // SIGNUP FORM
    const signupForm = document.getElementById("signupForm");

    if (signupForm) {
        signupForm.addEventListener("submit", function (event) {
            if (!signupForm.checkValidity()) {
                event.preventDefault();
                signupForm.reportValidity();
                return;
            }

            const password = signupForm.querySelector(
                '[name="password"]'
            );
            const confirmPassword = signupForm.querySelector(
                '[name="confirm_password"]'
            );

            if (
                password &&
                confirmPassword &&
                password.value !== confirmPassword.value
            ) {
                event.preventDefault();

                confirmPassword.setCustomValidity(
                    "The passwords do not match."
                );
                confirmPassword.reportValidity();
                return;
            }

            if (confirmPassword) {
                confirmPassword.setCustomValidity("");
            }

            const submitButton = signupForm.querySelector(
                'button[type="submit"]'
            );

            if (submitButton) {
                submitButton.disabled = true;

                const label = submitButton.querySelector("span");

                if (label) {
                    label.textContent = "Processing...";
                } else {
                    submitButton.textContent = "Processing...";
                }
            }
        });

        const confirmPassword = signupForm.querySelector(
            '[name="confirm_password"]'
        );

        if (confirmPassword) {
            confirmPassword.addEventListener("input", function () {
                confirmPassword.setCustomValidity("");
            });
        }
    }

    // OTP INPUT
    const otpInput = document.getElementById("otpInput");
    const otpForm = document.getElementById("otpForm");

    if (otpInput) {
        otpInput.addEventListener("input", function () {
            // Keep numeric digits only.
            otpInput.value = otpInput.value
                .replace(/\D/g, "")
                .slice(0, 6);

            otpInput.setCustomValidity("");
        });
    }

    // OTP FORM SUBMISSION
    if (otpForm && otpInput) {
        otpForm.addEventListener("submit", function (event) {
            const otp = otpInput.value.trim();

            if (!/^\d{6}$/.test(otp)) {
                event.preventDefault();

                otpInput.setCustomValidity(
                    "Enter the complete six-digit verification code."
                );

                otpInput.reportValidity();
                return;
            }

            otpInput.setCustomValidity("");

            const submitButton = otpForm.querySelector(
                'button[type="submit"]'
            );

            if (submitButton) {
                submitButton.disabled = true;

                const label = submitButton.querySelector("span");

                if (label) {
                    label.textContent = "Verifying...";
                }
            }
        });
    }
});


/* =========================================
   GOTogether LOGIN PAGE JAVASCRIPT
========================================= */

    // SHOW / HIDE PASSWORD
    const passwordInput = document.getElementById("loginPassword");
    const togglePassword = document.getElementById("togglePassword");
    const passwordEyeIcon = document.getElementById("passwordEyeIcon");

    if (passwordInput && togglePassword && passwordEyeIcon) {
        togglePassword.onclick = function () {
            const showPassword = passwordInput.type === "password";

            passwordInput.type = showPassword ? "text" : "password";
            passwordEyeIcon.className = showPassword
                ? "bi bi-eye-slash"
                : "bi bi-eye";

            togglePassword.setAttribute(
                "aria-label",
                showPassword ? "Hide password" : "Show password"
            );

            togglePassword.setAttribute(
                "aria-pressed",
                String(showPassword)
            );
        };

        console.log("GoTogether: Password toggle initialized.");
    } else {
        console.error("GoTogether: Password elements missing.", {
            passwordInput,
            togglePassword,
            passwordEyeIcon
        });
    }


/* ==========================================
   GoTogether Edit Profile Page
========================================== */

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("editProfileForm");

    if (!form) return;

    const licenseToggle = document.getElementById("id_has_driving_license");
    const licenseSection = document.getElementById("licenseDetailsSection");

    const vehicleToggle = document.getElementById("id_owns_vehicle");
    const vehicleSection = document.getElementById("vehicleDetailsSection");

    function toggleSection(toggle, section) {
        if (!toggle || !section) return;

        function update() {
            const enabled = toggle.checked;

            section.hidden = !enabled;

            section.querySelectorAll("input, select, textarea").forEach(function (field) {
                field.disabled = !enabled;
            });
        }

        toggle.addEventListener("change", update);
        update();
    }

    toggleSection(licenseToggle, licenseSection);
    toggleSection(vehicleToggle, vehicleSection);

    // Prevent accidental double submission.
    form.addEventListener("submit", function () {
        const saveButton = document.getElementById("saveProfileButton");

        if (saveButton && form.checkValidity()) {
            saveButton.disabled = true;
            saveButton.innerHTML =
                '<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>Saving...';
        }
    });
});

/* =========================================
   GoTogether Create Ride
   Vehicle, Helmet and Fuel Calculator
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("createRideForm");

    if (!form) return;

    const vehicleType = document.getElementById("id_vehicle_type");
    const totalSeats = document.getElementById("id_total_seats");
    const seatsHelp = document.getElementById("seatsHelp");

    const helmetNotice = document.getElementById("twoWheelerNotice");
    const spareHelmet = document.getElementById("id_has_spare_helmet");
    const helmetAgreement = document.getElementById("id_is_helmet_mandatory");
    const helmetWarning = document.getElementById("helmetWarning");

    const fuelCost = document.getElementById("id_total_estimated_fuel_cost");
    const costPerSeat = document.getElementById("id_cost_per_seat");
    const fuelSharePreview = document.getElementById("fuelSharePreview");
    const fuelCalculationNote = document.getElementById("fuelCalculationNote");

    const publishButton = document.getElementById("publishRideButton");

    /*
     * Vehicle detection.
     * Supports common choice values such as 2_WHEELER and 4_WHEELER.
     */
    function isTwoWheeler() {
        if (!vehicleType) return false;

        const value = String(vehicleType.value).toUpperCase();

        return (
            value.includes("2_WHEELER") ||
            value.includes("TWO_WHEELER") ||
            value === "BIKE" ||
            value === "SCOOTER" ||
            value === "2W"
        );
    }

    function updateVehicleRules() {
        if (!vehicleType || !totalSeats) return;

        const twoWheeler = isTwoWheeler();

        if (twoWheeler) {
            totalSeats.max = "1";

            if (Number(totalSeats.value) > 1) {
                totalSeats.value = "1";
            }

            if (seatsHelp) {
                seatsHelp.textContent =
                    "A 2-wheeler can offer a maximum of 1 pillion passenger seat.";
            }

            if (helmetNotice) {
                helmetNotice.hidden = false;
            }

            if (spareHelmet) spareHelmet.required = true;
            if (helmetAgreement) helmetAgreement.required = true;

        } else {
            totalSeats.removeAttribute("max");

            if (seatsHelp) {
                seatsHelp.textContent =
                    "Enter the number of available passenger seats for your vehicle.";
            }

            if (helmetNotice) {
                helmetNotice.hidden = true;
            }

            if (spareHelmet) spareHelmet.required = false;
            if (helmetAgreement) helmetAgreement.required = false;

            if (helmetWarning) {
                helmetWarning.hidden = true;
            }
        }

        updateFuelEstimate();
    }

    /*
     * Fuel split estimate:
     * total estimated fuel cost / (driver + planned passenger seats).
     *
     * The calculated value is a suggestion and can be edited by the user.
     */
    function updateFuelEstimate() {
        if (!fuelCost || !totalSeats || !fuelSharePreview) return;

        const total = Number(fuelCost.value);
        const seats = Number(totalSeats.value);

        if (
            fuelCost.value.trim() === "" ||
            !Number.isFinite(total) ||
            total <= 0 ||
            !Number.isFinite(seats) ||
            seats < 1
        ) {
            fuelSharePreview.textContent = "₹0.00";

            if (fuelCalculationNote) {
                fuelCalculationNote.textContent =
                    "Enter a positive fuel cost and passenger seat count to calculate an estimate.";
            }

            return;
        }

        const people = seats + 1;
        const share = total / people;

        fuelSharePreview.textContent = share.toLocaleString("en-IN", {
            style: "currency",
            currency: "INR",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

        if (fuelCalculationNote) {
            fuelCalculationNote.textContent =
                "Estimated using " + people +
                " people (driver + " + seats +
                " passenger seat" + (seats === 1 ? "" : "s") + ").";
        }

        // Fill a suggestion only when the field is empty.
        // The user can edit their own contribution amount.
        if (costPerSeat && costPerSeat.value.trim() === "") {
            costPerSeat.value = share.toFixed(2);
        }
    }

    if (vehicleType) {
        vehicleType.addEventListener("change", updateVehicleRules);
    }

    if (totalSeats) {
        totalSeats.addEventListener("input", updateFuelEstimate);
        totalSeats.addEventListener("change", updateFuelEstimate);
    }

    if (fuelCost) {
        fuelCost.addEventListener("input", updateFuelEstimate);
        fuelCost.addEventListener("change", updateFuelEstimate);
    }

    /*
     * Validate safety confirmations before submitting a 2-wheeler ride.
     */
    form.addEventListener("submit", function (event) {
        if (isTwoWheeler()) {
            const helmetConfirmed =
                spareHelmet && spareHelmet.checked &&
                helmetAgreement && helmetAgreement.checked;

            if (!helmetConfirmed) {
                event.preventDefault();

                if (helmetWarning) {
                    helmetWarning.hidden = false;
                }

                if (helmetNotice) {
                    helmetNotice.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });
                }

                return;
            }

            if (Number(totalSeats.value) > 1) {
                event.preventDefault();
                totalSeats.value = "1";
                updateFuelEstimate();

                if (seatsHelp) {
                    seatsHelp.textContent =
                        "A 2-wheeler can offer a maximum of 1 pillion passenger seat.";
                }

                totalSeats.focus();
                return;
            }
        }

        if (form.checkValidity()) {
            if (publishButton) {
                publishButton.disabled = true;
                publishButton.innerHTML =
                    '<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>Publishing Ride...';
            }
        } else {
            event.preventDefault();
            form.reportValidity();
        }
    });

    if (spareHelmet) {
        spareHelmet.addEventListener("change", function () {
            if (
                spareHelmet.checked &&
                helmetAgreement &&
                helmetAgreement.checked &&
                helmetWarning
            ) {
                helmetWarning.hidden = true;
            }
        });
    }

    if (helmetAgreement) {
        helmetAgreement.addEventListener("change", function () {
            if (
                spareHelmet &&
                spareHelmet.checked &&
                helmetAgreement.checked &&
                helmetWarning
            ) {
                helmetWarning.hidden = true;
            }
        });
    }

    // Initialize when the page loads, including saved form values.
    updateVehicleRules();
    updateFuelEstimate();
});


/* =========================================
   GoTogether - Edit Ride Page
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("editRideForm");
    const cancelButton = document.getElementById("cancelRideButton");

    if (!form) return;

    // Confirm before submitting a ride cancellation request.
    if (cancelButton) {
        cancelButton.addEventListener("click", function (event) {
            const message = cancelButton.dataset.confirm;

            if (message && !window.confirm(message)) {
                event.preventDefault();
            }
        });
    }

    // Prevent accidental repeated submissions.
    // Keep the cancellation button's name/value intact for Django.
    form.addEventListener("submit", function (event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            form.reportValidity();
            return;
        }

        const submitter = event.submitter;

        if (submitter && submitter.name === "cancel_ride") {
            return;
        }

        const saveButton = form.querySelector(
            ".edit-ride-save-btn"
        );

        if (saveButton) {
            saveButton.disabled = true;
            saveButton.innerHTML =
                '<i class="bi bi-arrow-repeat"></i> Saving Changes...';
        }
    });
});


/* =========================================
   GoTogether - Find Ride Page
========================================= */

document.addEventListener("DOMContentLoaded", function () {
    const filterForm = document.getElementById("findRideFilterForm");

    if (!filterForm) return;

    const searchButton = filterForm.querySelector(
        ".find-ride-submit-btn"
    );

    let searchSubmitted = false;

    filterForm.addEventListener("submit", function (event) {
        // Allow browser-native validation to run first.
        if (!filterForm.checkValidity()) {
            event.preventDefault();
            filterForm.reportValidity();
            return;
        }

        // Avoid submitting the same search multiple times.
        if (searchSubmitted) {
            event.preventDefault();
            return;
        }

        searchSubmitted = true;

        if (searchButton) {
            searchButton.disabled = true;
            searchButton.innerHTML =
                '<i class="bi bi-arrow-repeat"></i> Searching...';
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    const fareBox = document.getElementById("rrFareBox");
    const seatInput = document.getElementById("id_seats_booked");
    const fareDisplay = document.getElementById("totalFareDisplay");
    const fareSeats = document.getElementById("rrFareSeats");

    const knowsDriving = document.getElementById("id_knows_driving");
    const willingToSwap = document.getElementById("id_willing_to_swap");
    const licensePanel = document.getElementById("swapDrivingDetails");

    const requestForm = document.getElementById("requestRideForm");
    const submitButton = requestForm
        ? requestForm.querySelector('button[type="submit"]')
        : null;

    // Live fare calculation
    function updateFare() {
        if (!fareBox || !seatInput || !fareDisplay) {
            return;
        }

        const pricePerSeat = Number(fareBox.dataset.price);
        const seats = Number(seatInput.value);

        if (
            !Number.isFinite(pricePerSeat) ||
            !Number.isFinite(seats) ||
            seats < 1
        ) {
            fareDisplay.textContent = "—";
            if (fareSeats) {
                fareSeats.textContent = "Select seats";
            }
            return;
        }

        const total = pricePerSeat * seats;

        fareDisplay.textContent = total.toLocaleString("en-IN", {
            style: "currency",
            currency: "INR",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });

        if (fareSeats) {
            fareSeats.textContent =
                seats + (seats === 1 ? " seat" : " seats");
        }
    }

    if (seatInput) {
        seatInput.addEventListener("input", updateFare);
        seatInput.addEventListener("change", updateFare);
        updateFare();
    }

    // Expand licence details when the passenger can drive.
    function updateLicensePanel() {
        if (!licensePanel) {
            return;
        }

        const canDrive = Boolean(knowsDriving && knowsDriving.checked);

        licensePanel.hidden = !canDrive;

        const licenseNumber = document.getElementById("id_license_number");
        const licenseDocument = document.getElementById("id_license_document");

        if (licenseNumber) {
            licenseNumber.required = false;
        }

        if (licenseDocument) {
            licenseDocument.required = false;
        }
    }

    if (knowsDriving) {
        knowsDriving.addEventListener("change", updateLicensePanel);
    }

    // Do not silently submit a request claiming shift-sharing capability
    // without the passenger confirming that they can drive.
    if (willingToSwap && knowsDriving) {
        willingToSwap.addEventListener("change", function () {
            if (willingToSwap.checked && !knowsDriving.checked) {
                knowsDriving.checked = true;
                updateLicensePanel();
            }
        });

        knowsDriving.addEventListener("change", function () {
            if (!knowsDriving.checked) {
                willingToSwap.checked = false;
            }
        });
    }

    updateLicensePanel();

    // Prevent accidental double-click submissions.
    // The button is restored if native browser validation blocks submission.
    if (requestForm && submitButton) {
        requestForm.addEventListener("submit", function (event) {
            if (!requestForm.checkValidity()) {
                event.preventDefault();
                requestForm.reportValidity();
                return;
            }

            if (requestForm.dataset.submitting === "true") {
                event.preventDefault();
                return;
            }

            requestForm.dataset.submitting = "true";
            submitButton.disabled = true;
            submitButton.innerHTML =
                '<i class="bi bi-hourglass-split"></i> Sending Request...';
        });
    }
});

/* GoTogether - Ride Requests */

document.addEventListener("DOMContentLoaded", function () {
    const declineButtons = document.querySelectorAll(
        "[data-confirm-decline]"
    );

    declineButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            const confirmed = window.confirm(
                "Are you sure you want to decline this passenger request?"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});
