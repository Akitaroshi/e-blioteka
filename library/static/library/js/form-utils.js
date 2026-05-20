(function () {
    'use strict';

    function digitsOnly(value) {
        return value.replace(/\D/g, '');
    }

    function formatRussianPhone(value) {
        let d = digitsOnly(value);
        if (d.startsWith('7')) {
            d = '8' + d.slice(1);
        } else if (d.length && !d.startsWith('8')) {
            d = '8' + d;
        }
        d = d.slice(0, 11);

        if (!d.length) return '';
        if (d.length === 1) return '8';

        let out = '8(' + d.slice(1, 4);
        if (d.length <= 4) return out;
        out += ')' + d.slice(4, 7);
        if (d.length <= 7) return out;
        out += '-' + d.slice(7, 9);
        if (d.length <= 9) return out;
        out += '-' + d.slice(9, 11);
        return out;
    }

    function bindPhoneMask(input) {
        input.setAttribute('inputmode', 'numeric');
        input.setAttribute('autocomplete', 'tel');
        input.setAttribute('maxlength', '16');

        const apply = () => {
            const formatted = formatRussianPhone(input.value);
            if (input.value !== formatted) {
                input.value = formatted;
            }
        };

        input.addEventListener('input', apply);
        input.addEventListener('paste', () => setTimeout(apply, 0));
        input.addEventListener('blur', apply);
        if (input.value) apply();
    }

    function initPhoneMasks() {
        document.querySelectorAll('[data-phone-mask]').forEach(bindPhoneMask);
    }

    function checkPasswordRules(password, username) {
        const uname = (username || '').toLowerCase();
        const pwd = password || '';
        return {
            length: pwd.length >= 8,
            notNumeric: !/^\d+$/.test(pwd) || pwd.length === 0,
            notSimilar: !uname || pwd.length === 0 || !pwd.toLowerCase().includes(uname),
            hasLetter: /[A-Za-zА-Яа-яЁё]/.test(pwd) || pwd.length === 0,
        };
    }

    function renderRule(el, ok, idle) {
        const icon = idle ? '○' : (ok ? '✓' : '○');
        el.classList.toggle('text-emerald-600', ok && !idle);
        el.classList.toggle('text-slate-400', idle);
        el.classList.toggle('text-amber-600', !ok && !idle);
        el.querySelector('[data-rule-icon]').textContent = icon;
    }

    function initPasswordHints() {
        const box = document.getElementById('password-rules');
        const pwd = document.querySelector('[data-password-field]');
        const user = document.querySelector('[data-username-field]');
        if (!box || !pwd) return;

        const rules = {
            length: box.querySelector('[data-rule="length"]'),
            notNumeric: box.querySelector('[data-rule="notNumeric"]'),
            notSimilar: box.querySelector('[data-rule="notSimilar"]'),
            hasLetter: box.querySelector('[data-rule="hasLetter"]'),
        };

        const update = () => {
            const r = checkPasswordRules(pwd.value, user ? user.value : '');
            const idle = !pwd.value;
            Object.keys(rules).forEach((key) => {
                if (rules[key]) renderRule(rules[key], r[key], idle);
            });
        };

        pwd.addEventListener('input', update);
        if (user) user.addEventListener('input', update);
        update();
    }

    document.addEventListener('DOMContentLoaded', () => {
        initPhoneMasks();
        initPasswordHints();
    });
})();
