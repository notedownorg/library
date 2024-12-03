# Copyright 2024 Notedown Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

hygiene: tidy gen format licenser

# Shared things
licenser:
	nix develop --command licenser apply -r "Notedown Authors"

dirty:
	nix develop --command git diff --exit-code

# Golang things
run:
	nix develop --command go run main.go

install:
	nix develop --command go install -ldflags "-X 'github.com/notedownorg/library/cmd.CommitHash=$(shell git rev-parse HEAD)'"

tidy:
	nix develop --command go mod tidy

gen:
	nix develop --command go generate ./...

test:
	nix develop --command go test ./...

format:
	nix develop --command gofmt -w .

# Python things
# TODO nix this
# install:
	# poetry install --directory ./plugins/extract
#
# bundle:
	# poetry run --directory ./plugins/extract bundle
#
# serve:
	# @poetry run --directory ./plugins/extract server
