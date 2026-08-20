import Link from 'next/link';

export default function Nav() {
  return (
    <nav className="nav">
      <div className="container nav__inner">
        <Link className="nav__logo" href="/">
          nstate
        </Link>
        <ul className="nav__links">
          <li>
            <Link className="nav__link" href="/ask">ask</Link>
          </li>
          <li>
            <Link className="nav__link" href="/scorecards">scorecards</Link>
          </li>
          <li>
            <Link className="nav__link" href="/uk">UK</Link>
          </li>
          <li>
            <Link className="nav__link" href="/eu">EU</Link>
          </li>
          <li>
            <a
              aria-label="nstate on GitHub"
              className="nav__link"
              href="https://github.com/nstate-project/nstate"
              rel="noopener noreferrer"
              target="_blank"
            >
              github ↗
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
}
