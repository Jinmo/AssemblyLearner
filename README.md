# AssemblyLearner
Self-contained judge program for assembly language (supports x86). This runs [0e1.kr](http://0e1.kr).

## Installation

```bash
git clone https://github.com/Jinmo/AssemblyLearner.git asmlearner
cd asmlearner; ./install.sh
```

### Adding a challenge

0. Create admin account: `python manage.py admin`
0. Login and go admin menu -> challenge menu

## Dependencies
- Python 2.7 + virtualenv
- PostgreSQL
- Celery
- see requirements.txt for details