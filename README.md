# IGNOU Question Paper Downloader

A Python tool to download previous year question papers for IGNOU (Indira Gandhi National Open University) students, specifically designed for BCA/MCA courses.

## 🚀 Features

- **Batch Download**: Download multiple course question papers at once
- **Year Range**: Supports question papers from 2005 to 2018
- **Session Support**: Downloads both June and December session papers
- **PDF Merging**: Option to merge downloaded PDFs by course
- **Progress Tracking**: Real-time progress bar for downloads
- **Error Handling**: Robust error handling for network issues
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

- Python 3.7 or higher
- Internet connection
- IGNOU course codes

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/samirank/qp_downloader.git
   cd qp_downloader
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Dependencies

The following packages are required:
- `urllib3` - HTTP client for downloading files
- `beautifulsoup4` - HTML parsing
- `PyPDF2` - PDF manipulation and merging
- `pathlib` - Path operations (included in Python 3.4+)

## 🎯 Usage

### Basic Usage

Run the main script:
```bash
python qp_downloader.py
```

### Interactive Mode

1. Enter course codes when prompted (separate multiple codes with spaces)
2. Choose whether to merge PDFs for each course
3. The tool will automatically:
   - Fetch available sessions
   - Download question papers
   - Organize files by year and month
   - Merge PDFs if requested

### Example Course Codes

Common IGNOU course codes:
- `BCA-001` - Computer Basics and PC Software
- `BCA-002` - Programming in C
- `BCA-003` - Computer Organization
- `BCA-004` - Mathematics for Computing
- `BCA-005` - Business Communication

## 📁 Project Structure

```
qp_downloader/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── qp_downloader.py      # Main entry point
├── download.py           # Core download functionality
├── progress.py           # Progress bar utility
├── .gitignore           # Git ignore file
└── LICENSE              # MIT License
```

## 🔧 Configuration

You can customize the tool by modifying the source code:

- **Year Range**: Modify the `get_range()` function in `download.py` to change supported years
- **Session Types**: Update the months list in `download.py` to add/remove session types
- **School Codes**: Change the default school code in `qp_downloader.py`
- **Download Path**: Modify the path variable in `download.py`
- **Timeout Settings**: Adjust network timeouts in the `get_html()` function

## 🐛 Troubleshooting

### Common Issues

1. **Connection Errors**: Check your internet connection
2. **Permission Errors**: Ensure write permissions in download directory
3. **Missing Dependencies**: Run `pip install -r requirements.txt`
4. **PDF Merge Errors**: Ensure PyPDF2 is properly installed
5. **Dependency Confusion**: This project uses `PyPDF2`, not `py2pdf`. Make sure to install the correct package.

### Error Codes

- `-1`: Unable to connect to server
- `-2`: Connection timed out

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Samiran Kakoty**
- GitHub: [@samirank](https://github.com/samirank)
- Project: [qp_downloader](https://github.com/samirank/qp_downloader)

## 🙏 Acknowledgments

- IGNOU for providing access to question papers
- The open-source community for various libraries used
- Contributors and users of this tool

## 📊 Supported Years and Sessions

- **Years**: 2005-2018
- **Sessions**: June, December
- **School**: SOCIS (School of Computer and Information Sciences)

## ⚠️ Disclaimer

This tool is for educational purposes only. Please respect IGNOU's terms of service and use the downloaded materials responsibly.

---

⭐ If you find this tool helpful, please give it a star on GitHub!
