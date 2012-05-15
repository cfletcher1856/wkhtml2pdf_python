from random import randint
import subprocess


class html2pdf(object):
    _html = None
    url = None
    _input = None
    cmd = None
    tmp = None
    pdf = None
    builtinfuncs = None
    pdf_file = None

    def __init__(self):
        self.get_cpu()
        self.cmd = '/usr/local/bin/wkhtmltopdf-{0}'.format(self.cpu)
        self.tmp = '/tmp/{0}.html'.format(randint(1, 100000))
        self.builtinfuncs = dir(self)

    def get_cpu(self):
        amd = ["grep -i amd /proc/cpuinfo"]
        intel = ["grep -i intel /proc/cpuinfo"]
        if self.execute(amd):
            self.cpu = 'amd64'
        elif self.execute(intel):
            self.cpu = 'i386'
        else:
            raise Exception('Could not determine CPU')

    def execute(self, command):
        try:
            proc = subprocess.check_output(' '.join(command), shell=True)
            return proc
        except Exception:
            print "exception"
            raise

    def html(self, html):
        self._html = html
        f = open(self.tmp, 'w')
        f.write(html)
        f.close()

    @property
    def help(self):
        print self.execute([self.cmd, '--extended-help'])

    @property
    def version(self):
        print self.execute([self.cmd, '--version'])

    @property
    def man(self):
        print self.execute([self.cmd, '--manpage'])

    def render(self):
        params = ['collate', 'no_collate', 'cookie_jar', 'copies', 'dpi',
            'extended_help', 'grayscale', 'help', 'htmldoc', 'image_dpi',
            'image_quality', 'lowquality', 'manpage', 'margin_bottom', 'margin_left',
            'margin_right', 'margin_top', 'orientation', 'output_format', 'page_height',
            'page_size', 'page_width', 'no_pdf_compression', 'quiet',
            'read_args_from_stdin', 'readme', 'title', 'use_xserver', 'version',
            'dump_default_toc_xsl', 'dump_outline', 'outline', 'no_outline',
            'outline_depth', 'allow', 'background', 'no_background',
            'checkbox_checked_svg', 'checkbox_svg', 'cookie', 'custom_header',
            'custom_header_propagation', 'no_custom_header_propagation',
            'debug_javascript', 'no_debug_javascript', 'default_header', 'encoding',
            'disable_external_links', 'enable_external_links', 'disable_forms',
            'enable_forms', 'images', 'no_images', 'disable_internal_links',
            'enable_internal_links', 'disable_javascript', 'enable_javascript',
            'javascript_delay', 'load_error_handling', 'disable_local_file_access',
            'enable_local_file_access', 'minimum_font_size', 'exclude_from_outline',
            'include_in_outline', 'page_offset', 'password', 'disable_plugins',
            'enable_plugins', 'post', 'post_file', 'print_media_type',
            'no_print_media_type', 'proxy', 'radiobutton_checked_svg', 'run_script',
            'disable_smart_shrinking', 'enable_smart_shrinking', 'stop_slow_scripts',
            'no_stop_slow_scripts', 'disable_toc_back_links', 'enable_toc_back_links',
            'user_style_sheet', 'username', 'window_status', 'zoom', 'footer_center',
            'footer_font_name', 'footer_font_size', 'footer_html', 'footer_left',
            'footer_line', 'no_footer_line', 'footer_right', 'footer_spacing',
            'header_center', 'header_font_name', 'header_font_size', 'header_html',
            'header_left', 'header_line', 'no_header_line', 'header_right',
            'header_spacing', 'replace', 'disable_dotted_lines', 'toc_header_text',
            'toc_level_indentation', 'disable_toc_links', 'toc_text_size_shrink',
            'xsl_style_sheet', 'cover']
        wrapthese = ['title', 'footer_center', 'footer_left', 'footer_right',
            'header_center', 'header_right', 'header_left', 'toc_header_text']
        escapethese = ['cover']
        realparams = [self.cmd]

        for p in dir(self):
            if p in self.builtinfuncs:
                continue
            if not p in params:
                raise Exception("%s is not a valid attribute." % p)

            val = getattr(self, p)

            if p in escapethese:
                realparams.append(p)
            else:
                realparams.append('--' + p)

            if val is None:
                continue
            if isinstance(val, str):
                if p in wrapthese:
                    realparams.append('"' + val + '"')
                else:
                    realparams.append(val)
            else:
                realparams.append(repr(val))

        realparams = [param.replace('_', '-') for param in realparams]

        if self.url:
            self._input = self.url
        elif self._html:
            self._input = self.tmp
        else:
            raise Exception("You need to specify a url or html")

        realparams.append(self._input)
        realparams.append('-')

        self.pdf = self.execute(realparams)

    def output(self, mode):
        modes = {
            'download': self.download_pdf,
            'string': self.string_pdf,
            'save': self.save_pdf,
        }

        return modes.get(mode, self.bad_mode)()

    def download_pdf(self):
        raise NotImplementedError("Need to finish or not use at all")

    def string_pdf(self):
        return self.pdf

    def save_pdf(self):
        if not self.pdf_file:
            raise Exception("You need to set pdf_file")

        f = open(self.pdf_file, 'w')
        f.write(self.pdf)
        f.close()

    def bad_mode(self):
        raise Exception("Please use download, string or save")


w = html2pdf()
w.cover = 'protectamerica.com'
w.url = "http://www.google.com"
w.render()
w.pdf_file('cover.pdf')
w.output('save')
