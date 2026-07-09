function Footer({ darkMode }) {
  return (
    <footer className={`border-t px-4 py-6 text-center text-sm ${darkMode ? 'border-slate-800 text-slate-400' : 'border-slate-200 text-slate-600'}`}>
      <p>Secure audio assessment with transparent processing, privacy-first defaults, and practical feedback.</p>
    </footer>
  );
}

export default Footer;
