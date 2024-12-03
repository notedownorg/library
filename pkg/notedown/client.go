// Copyright 2024 Notedown Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package notedown

import (
	"time"

	"github.com/notedownorg/notedown/pkg/fileserver/reader"
	"github.com/notedownorg/notedown/pkg/fileserver/writer"
	"github.com/notedownorg/notedown/pkg/providers/source"
)

type SourceWriter interface {
	NewSourceLocation(title string) string
	CreateSource(path string, title string, format source.Format, url string, options ...source.SourceOption) error
}

type Client interface {
	SourceWriter
}

type client struct {
	*source.SourceClient
}

func NewClient(root string) (Client, error) {
	read, err := reader.NewClient(root, "task")
	if err != nil {
		return nil, err
	}
	write := writer.NewClient(root)

	sourceReaderChannel := make(chan reader.Event)
	read.Subscribe(sourceReaderChannel, reader.WithInitialDocuments())
	sourceClient := source.NewClient(write, sourceReaderChannel, source.WithInitialLoadWaiter(100*time.Millisecond))

	return &client{
		SourceClient: sourceClient,
	}, nil
}
