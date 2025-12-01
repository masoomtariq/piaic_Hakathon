import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'Bridging the digital brain and the physical body',
  favicon: 'img/favicon.ico',

  // Vercel deployment root
  url: 'https://giaic-q4-hackathon-physical-ai-and.vercel.app',
  baseUrl: '/',

  organizationName: 'Okashanadeem',
  projectName: 'GIAIC-Q4-Hackathon-Physical-AI-and-Humanoid-Robotics-Textbook',

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn', // v4-compatible
    },
  },

  customFields: {
    chatbotBackendUrl: process.env.REACT_APP_CHATBOT_BACKEND_URL || 'http://localhost:8000',
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  future: {
    v4: true,
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/Okashanadeem/GIAIC-Q4-Hackathon-Physical-AI-and-Humanoid-Robotics-Textbook',
        },
        blog: {
          showReadingTime: true,
          feedOptions: { type: ['rss', 'atom'], xslt: true },
          editUrl:
            'https://github.com/Okashanadeem/GIAIC-Q4-Hackathon-Physical-AI-and-Humanoid-Robotics-Textbook',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: { customCss: './src/css/custom.css' },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: { respectPrefersColorScheme: true },
    navbar: {
      title: 'Physical AI & Humanoid Robotics Textbook',
      logo: { alt: 'Physical AI Logo', src: 'img/logo.svg' },
      items: [
        { type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Textbook' },
        { href: 'https://github.com/Okashanadeem/GIAIC-Q4-Hackathon-Physical-AI-and-Humanoid-Robotics-Textbook', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        { title: 'Docs', items: [{ label: 'Textbook', to: '/docs/introduction' }] },
        { title: 'Community', items: [{ label: 'GitHub', href: 'https://github.com/Okashanadeem/GIAIC-Q4-Hackathon-Physical-AI-and-Humanoid-Robotics-Textbook' }] },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Okasha Nadeem. Built with Docusaurus.`,
    },
    prism: { theme: prismThemes.github, darkTheme: prismThemes.dracula },
  } satisfies Preset.ThemeConfig,
};

export default config;
