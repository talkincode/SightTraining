# 定义变量
DIST_DIR=dist
BUILD_DIR=build
BUILD_CMD=python setup.py sdist bdist_wheel
CLEAN_CMD=rm -rf $(DIST_DIR) $(BUILD_DIR) *.egg-info
WHL_FILE=$(wildcard $(DIST_DIR)/*.whl)
PACKAGE_NAME=sight-training
UPLOAD_CMD=twine upload $(DIST_DIR)/*

# 默认目标
.PHONY: all
all: clean build

# 构建项目
.PHONY: build
build: clean
	$(BUILD_CMD)

# 清理构建产物
.PHONY: clean
clean:
	find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
	$(CLEAN_CMD)

# 安装包
.PHONY: install
install:
	@if [ -z "$(WHL_FILE)" ]; then \
		echo "No .whl file found in $(DIST_DIR). Please run 'make build' first."; \
	else \
		pip install $(WHL_FILE); \
	fi

# 卸载包
.PHONY: uninstall
uninstall:
	pip uninstall -y $(PACKAGE_NAME)

# 上传包到 PyPI
.PHONY: upload
upload:
	$(UPLOAD_CMD)

app:
	pyinstaller spacex01.spec

# 帮助信息
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  build     - Build the package."
	@echo "  clean     - Remove build artifacts."
	@echo "  install   - Install the package using the built wheel file."
	@echo "  uninstall - Uninstall the package."
	@echo "  upload    - Upload the package to PyPI."
	@echo "  all       - Clean the build environment and then build the package."
	@echo "  help      - Show this help message."